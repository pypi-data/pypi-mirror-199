#include <functional>
#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include "algorithms.h"

namespace py = pybind11;

typedef std::function<py::array_t<double>(py::array_t<double>)> pyfunction;

dopt::matrix<double> pyarray2matrix(py::array_t<double> x) {
	py::buffer_info buf(x.request());
	int m(buf.shape[0]), n(1);
	if (buf.ndim >= 2)
		n = buf.shape[1];
	dopt::matrix<double> p_x(m, n);
	if (buf.size) {
		if (buf.ndim == 1) {
			std::copy((double*)buf.ptr, (double*)buf.ptr + buf.size, p_x.begin());
        }
		else {
			dopt::matrix<double>::iterator it(p_x.begin());
			for (int i(0); i < n; ++i)
				for (int j(0); j < m; ++j, ++it)
					*it = *((double*)((char*)buf.ptr + i*buf.strides[1] + j*buf.strides[0]));
		}
    }
	return p_x;
}

py::array matrix2pyarray(const dopt::matrix<double>& x, size_t ndim) {
	std::vector<size_t> strides;
	std::vector<size_t> shape;
	if (ndim == 1) {
		strides = { sizeof(double) };
		shape = { (size_t)x.size(1) };
	}
	else
		if (ndim == 2) {
			strides = { sizeof(double), x.size(1) * sizeof(double) };
			shape = { (size_t)x.size(1), (size_t)x.size(2) };
		}
		else 
			if (ndim == 3) {
				strides = { sizeof(double), x.size(1) * sizeof(double), x.size(1) * x.size(2) * sizeof(double) };
				shape = { (size_t)x.size(1), (size_t)x.size(2), (size_t)x.size(3) };
			}
	py::array p_x;
	if (x.empty())
		p_x = py::array(py::buffer_info(0, sizeof(double), py::format_descriptor<double>::format(), ndim, shape, strides));
	else
		p_x = py::array(py::buffer_info((void*)&x(0), sizeof(double), py::format_descriptor<double>::format(), ndim, shape, strides));
	return p_x;
}


struct pyfunction_wrapper {
	pyfunction m_f;

	pyfunction_wrapper(const pyfunction& f) : m_f(f) {}

	dopt::matrix<double> operator()(const dopt::matrix<double>& x) {
		return pyarray2matrix(m_f(matrix2pyarray(x, 2)));
	}
};

struct bindf {
	std::function<double(double)> m_f;

	bindf(const std::function<double(double)>& f) : m_f(f) {}

	dopt::matrix<double> operator()(const dopt::matrix<double>& x) {
		return dopt::matrix<double>(1, 1, m_f(x(0)));
	}
};

double gs(const std::function<double(double)> &f, double a, double b, double epsilon, int n_max) {
	return dopt::golden_section(bindf(f), a, b, epsilon, n_max);
}

py::tuple em(pyfunction p_f, pyfunction p_df, pyfunction p_g, pyfunction p_dg, py::array_t<double> p_A, py::array_t<double> p_b, py::array_t<double> p_Aeq, py::array_t<double> p_beq, py::array_t<double> p_xmin, py::array_t<double> p_xmax, py::array_t<double> p_x0, py::array_t<double> p_Q0, double epsilon, int kmax, int kimax, double shallowcut, bool decomposition, bool memory, bool log) {
	// type definitions
	typedef dopt::matrix<double> M;

	// matrices
	M A(pyarray2matrix(p_A)), b(pyarray2matrix(p_b));
	M Aeq(pyarray2matrix(p_Aeq)), beq(pyarray2matrix(p_beq));
	M xmin(pyarray2matrix(p_xmin)), xmax(pyarray2matrix(p_xmax));
	M x(pyarray2matrix(p_x0)), fx(0, 0), Qi(pyarray2matrix(p_Q0));

	// error check
	if (A.dimension() != 2 || Aeq.dimension() != 2)
		throw std::runtime_error("Number of dimensions of A and Aeq must be two.");
	if (xmin.size(1) != xmax.size(1) || A.size(1) != b.size(1) || Aeq.size(1) != beq.size(1) || A.size(2) != xmin.size(1) || Aeq.size(2) != xmin.size(1))
		throw std::runtime_error("Inconsistent input matrix dimensions.");

	// functions
	pyfunction_wrapper f(p_f), df(p_df), g(p_g), dg(p_dg);

	// solution
	int stop;
	std::pair<M, M> emr(dopt::ellipsoid(f, df, g, dg, A, b, Aeq, beq, xmin, xmax, x, fx, Qi, stop, epsilon, kmax, kimax, shallowcut, decomposition, memory, log));
	M xb(emr.first), fxb(emr.second);

	// return
	py::array p_xb(matrix2pyarray(xb, 2)), p_fxb(matrix2pyarray(fxb, 2)), p_x((matrix2pyarray(x, 2))), p_fx(matrix2pyarray(fx, 2)), p_Q(matrix2pyarray(Qi, 3));
	return py::make_tuple(p_xb, p_fxb, p_x, p_fx, p_Q, stop);
}


PYBIND11_MODULE(nlpalg, m) {
	m.def("goldensection", &gs, "Golden section univariate algorithm");
	m.def("ellipsoidmethod", &em, "Ellipsoid method multivariate algorithm");
}
