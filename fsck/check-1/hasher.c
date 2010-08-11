#include <sys/stat.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <openssl/sha.h>
#include <fcntl.h>
#include <Python.h>

#define SHA1SIZE 20


static PyObject *HasherError;

#define py_err(_in_where_, _in_what_) \
{ \
	const char * _where_ = _in_where_; \
	const char * _what_ = _in_what_; \
	PyObject *s; \
	\
	Py_BLOCK_THREADS; \
	if (_what_) \
		s = PyString_FromFormat("%s (%s): %s.", _where_, _what_, strerror(errno)); \
	else \
		s = PyString_FromFormat("%s: %s.", _where_, strerror(errno)); \
	PyErr_SetObject(HasherError, s); \
	\
	goto done;\
}; \

static PyObject *hash_file(PyObject *self, PyObject *args)
{
	const char *filename;
	int fd;
	struct stat st_buf;
	unsigned char *map;
	unsigned char obuf[SHA1SIZE];
	SHA_CTX ctx;
	PyObject *res = NULL;
	PyThreadState *_save;
	char res_s[2*SHA1SIZE + 1];
	int r;

	if (!PyArg_ParseTuple(args, "s", &filename))
		goto done;

	/** release GIL **/
	Py_UNBLOCK_THREADS;

	fd = open(filename, O_RDONLY | O_LARGEFILE);
	if (fd < 0) py_err("Cannot open file", filename);
	if (fstat(fd, &st_buf) < 0) py_err("Cannot fstat file", filename);

	posix_fadvise(fd, 0, 0, POSIX_FADV_NOREUSE);
	//posix_fadvise(fd, 0, 0, POSIX_FADV_WILLNEED);
	posix_fadvise(fd, 0, 0, POSIX_FADV_SEQUENTIAL);

	if (SHA1_Init(&ctx) != 1)
		py_err("SHA1_Init()", NULL);

	map = mmap(NULL, st_buf.st_size, PROT_READ, MAP_SHARED, fd, 0);
	if (map == MAP_FAILED) py_err("mmap failed", filename);

	//posix_madvise(map, st_buf.st_size, POSIX_MADV_WILLNEED);
	posix_madvise(map, st_buf.st_size, POSIX_MADV_SEQUENTIAL);

	if (SHA1_Update(&ctx, map, st_buf.st_size) != 1)
		py_err("SHA1_Update", NULL);

	posix_madvise(map, st_buf.st_size, POSIX_MADV_DONTNEED);
	if (munmap(map, st_buf.st_size) < 0) py_err("munmap failed", filename);
	posix_fadvise(fd, 0, 0, POSIX_FADV_DONTNEED);
	if (close(fd) < 0)
		py_err("Cannot close bar", filename);
	if (SHA1_Final(obuf, &ctx) != 1)
		py_err("SHA1_Final", NULL);

	r = snprintf(res_s, sizeof(res_s),
	             "%02x%02x%02x%02x%02x"
	             "%02x%02x%02x%02x%02x"
	             "%02x%02x%02x%02x%02x"
	             "%02x%02x%02x%02x%02x",
	    obuf[ 0], obuf[ 1], obuf[ 2], obuf[ 3], obuf[ 4],
	    obuf[ 5], obuf[ 6], obuf[ 7], obuf[ 8], obuf[ 9],
	    obuf[10], obuf[11], obuf[12], obuf[13], obuf[14],
	    obuf[15], obuf[16], obuf[17], obuf[18], obuf[19]);
	if (r >= sizeof(res_s)) {
		printf("%d vs %ld\n", r, sizeof(res_s));
		py_err("snprintf failure", filename);
	}

	/** reacquire GIL **/
	Py_BLOCK_THREADS
	return PyString_FromStringAndSize(res_s, sizeof(res_s)-1);

done:
	return res;
}

static PyMethodDef HasherMethods[] = {
	{"hash_file",  hash_file, METH_VARARGS, "Hash a file"},
	{NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC inithasher(void) {
	PyObject *module;

	module = Py_InitModule("hasher", HasherMethods);
	if (!module) return;

	HasherError = PyErr_NewException("hasher.error", NULL, NULL);
	Py_INCREF(HasherError);
	PyModule_AddObject(module, "error", HasherError);
}

// vim:set ts=4:
// vim:set shiftwidth=4:
