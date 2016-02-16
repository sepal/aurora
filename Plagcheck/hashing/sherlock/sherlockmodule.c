#include <Python.h>
#include "sherlock.h"

#define MAX_HASH_BUFFER_SIZE 255

static PyObject *
sherlock_signature(PyObject *self, PyObject *args)
{
    int i;
    const char *filepath;
    Sig *ret_sig;

    if (!PyArg_ParseTuple(args, "s", &filepath))
        return NULL;

    ret_sig = signature_file(filepath);

    PyObject* list = PyList_New(0);

    for (i = 0; i < ret_sig->nval; i++) {
        static char sigbuf[MAX_HASH_BUFFER_SIZE];
        snprintf(sigbuf, MAX_HASH_BUFFER_SIZE, "%lx", ret_sig->val[i]);
        PyObject *val = Py_BuildValue("s", sigbuf);
        PyList_Append(list, val);
    }

    return list;
}

static PyObject *
sherlock_signature_str(PyObject *self, PyObject *args)
{
    int i;
    char *text;
    Sig *ret_sig;

    if (!PyArg_ParseTuple(args, "s", &text))
        return NULL;

    ret_sig = signature_str(text);

    PyObject* list = PyList_New(0);

    for (i = 0; i < ret_sig->nval; i++) {
        static char sigbuf[MAX_HASH_BUFFER_SIZE];
        snprintf(sigbuf, MAX_HASH_BUFFER_SIZE, "%lx", ret_sig->val[i]);
        PyObject *val = Py_BuildValue("s", sigbuf);
        PyList_Append(list, val);
    }

    return list;
}

static PyMethodDef module_methods[] = {
    {"signature",  sherlock_signature, METH_VARARGS, "Create a signature from file."},
    {"signature_str", sherlock_signature_str, METH_VARARGS, "Create a signature from string."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef sherlock =
{
    PyModuleDef_HEAD_INIT,
    "sherlock", /* name of module */
    "Plagiarism detection hashing algorithm. No multithreading support.",
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC PyInit_sherlock(void)
{
    return PyModule_Create(&sherlock);
}