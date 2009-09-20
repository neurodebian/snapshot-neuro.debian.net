#!/usr/bin/python
#
# Copyright (c) 2009 Peter Palfrader
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def upgrade(db):
    """Handle symlinks"""
    db.execute("""
        CREATE OR REPLACE FUNCTION stat(VARCHAR, INTEGER) RETURNS stat_result AS $$
            BEGIN { strict->import(); }

            my ($path, $mirrorrun_id) = @_;

            my $res;
            my $query_mirrorrun;
            my $query_directory;
            my $query_file;
            my $query_symlink;
            my $result;
            my $recurse_depth = 0;

            $query_mirrorrun = spi_prepare('SELECT run, archive_id FROM mirrorrun WHERE mirrorrun_id = $1', 'INTEGER');
            $res = spi_query_prepared($query_mirrorrun, $mirrorrun_id);
            my $run = spi_fetchrow($res);
            goto done unless (defined $run);

            # A couple of prepares.  We already need to query directories,
            # so that right now.  File and symlink we only need sometimes,
            # so write the code here, but call later if necessary.
            $query_directory = spi_prepare('
               SELECT directory_id, node_with_ts.node_id
                  FROM directory JOIN node_with_ts ON directory.node_id = node_with_ts.node_id
                  WHERE path=$1
                    AND node_with_ts.archive_id = $2
                    AND first_run <= $3
                    AND last_run  >= $3
                ', 'VARCHAR', 'INTEGER', 'TIMESTAMP') unless defined $query_directory;

            my $get_query_file = sub {
                $query_file = spi_prepare('
                    SELECT node_with_ts2.node_id, file.hash, file.size
                      FROM file NATURAL JOIN node_with_ts2
                      WHERE parent=$1
                        AND first_run <= $2
                        AND last_run  >= $2
                        AND name=$3
                    ', 'INTEGER', 'TIMESTAMP', 'VARCHAR') unless defined $query_file;
                return $query_file;
            };
            my $get_query_symlink = sub {
                $query_symlink = spi_prepare('
                SELECT node_with_ts2.node_id, symlink.target
                  FROM symlink NATURAL JOIN node_with_ts2
                  WHERE parent=$1
                    AND first_run <= $2
                    AND last_run  >= $2
                    AND name=$3
                ', 'INTEGER', 'TIMESTAMP', 'VARCHAR') unless defined $query_symlink;
                return $query_symlink;
            };

            my $cleanup_path = sub {
                my $changed;
                do {
                    $changed = 0;
                    $changed += $path =~ s#//#/#g;
                    $changed += $path =~ s#/\./#/#g;
                    $changed += $path =~ s#^/\.\./#/#g;
                    $changed += $path =~ s#/([^/]+)/\.\.(/|$)#/#;
                } while ($changed > 0);
                $path =~ s#(/$)##;
                if ($path eq '') {
                    $path = '/';
                    last;
                };
            };



            syml:
            while(1) {
                if ($recurse_depth++ >= 10) {
                    # way too many symlinks in the chain
                    goto done;
                };

                # ok, if it is a directory that will be quite easy:
                $res = spi_query_prepared($query_directory, $path, $run->{'archive_id'}, $run->{'run'});
                my $dir = spi_fetchrow($res);
                if (defined $dir) {
                    $result = {'filetype'=>'d', 'path'=>$path, 'directory_id'=>$dir->{'directory_id'}, 'node_id'=>$dir->{'node_id'}};
                    goto done;
                };

                # ok, so not.  maybe it is a normal file...
                my ($dirname, $basename) = $path =~ m#(.*)/(.*)#;
                $dirname = '/' if ($dirname eq '');

                # check if that directory exists,
                $res = spi_query_prepared($query_directory, $dirname, $run->{'archive_id'}, $run->{'run'});
                my $dir = spi_fetchrow($res);
                if (defined $dir) {
                    # and if it has a plain file like we want in it
                    $res = spi_query_prepared(&$get_query_file, $dir->{'directory_id'}, $run->{'run'}, $basename);
                    my $file = spi_fetchrow($res);
                    if (defined $file) {
                        $result = {'filetype'=>'-', 'path'=>$path, 'digest'=>$file->{'hash'}, 'node_id'=>$file->{'node_id'}, 'size'=>$file->{'size'}};
                        goto done;
                    };

                    # ok, no plain file, but maybe a symlink?
                    $res = spi_query_prepared(&$get_query_symlink, $dir->{'directory_id'}, $run->{'run'}, $basename);
                    my $symlink = spi_fetchrow($res);
                    if (defined $symlink) {
                        $path = $dirname . '/' . $symlink->{'target'};
                        &$cleanup_path;
                        next syml;
                    };
                };

                # maybe there is a symlink in the path.
                $dirname =~ s#^/##;
                my @path_parts = split('/', $dirname);
                my @done_parts = ();
                my $dir = '/';
                while (scalar @path_parts > 0) {
                    my $this_dir = '/' . join('/', @done_parts);
                    my $this_base = shift @path_parts;
                    push @done_parts, $this_base;

                    # does this directory exist?
                    $res = spi_query_prepared($query_directory, $this_dir, $run->{'archive_id'}, $run->{'run'});
                    my $dir = spi_fetchrow($res);
                    if (defined $dir) {
                        # is our next path element a symlink?
                        $res = spi_query_prepared(&$get_query_symlink, $dir->{'directory_id'}, $run->{'run'}, $this_base);
                        my $symlink = spi_fetchrow($res);
                        if (defined $symlink) {
                            # yes.  replace it with the symlink target and go again.
                            $path = $this_dir . '/' . $symlink->{'target'} . '/' . join('/', @path_parts) . '/' . $basename;
                            &$cleanup_path;
                            next syml;
                        };
                        # nope.  Well, maybe next time.
                    } else {
                        # our dir doesn't exist as a directory?  Well, then this can't be a valid symlink either.
                        goto done;
                    };
                };
            };
        done:
            spi_freeplan($query_mirrorrun) if defined $query_mirrorrun;
            spi_freeplan($query_directory) if defined $query_directory;
            spi_freeplan($query_file) if defined $query_file;
            spi_freeplan($query_symlink) if defined $query_symlink;
            return $result;
        END;
        $$ LANGUAGE plperl;
        """)

    db.execute("UPDATE config SET value='7' WHERE name='db_revision' AND value='6'")

# vim:set et:
# vim:set ts=4:
# vim:set shiftwidth=4:
