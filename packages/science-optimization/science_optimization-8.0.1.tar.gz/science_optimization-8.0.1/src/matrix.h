#ifndef _MATRIX_H_
#define _MATRIX_H_

#include <vector>
#include <limits>
#include <cmath>
#include <cstdlib>


namespace dopt {

	// constants
	const double pi = 3.141592653589793; // circle constant
	const double inf = std::numeric_limits<double>::infinity(); // infinity

	// functions
	template <class T, class P> T prod(P p, P pe, T r=1) {
		while (p != pe)
			r *= *(p++);
		return r;
	}
	template <class T> T min(const T& a, const T& b) {
		return a < b ? a : b;
	}
	template <class T> T max(const T& a, const T& b) {
		return a > b ? a : b;
	}
	template <class P> void swap(P it, P ite, P itd) {
		while (it != ite)
			std::swap(*(it++), *(itd++));
	}

	// full matrix
	template <class T> class matrix {
	private:
		// matrix data
		std::vector<int> m_dimension; // matrix dimension
		std::vector<T> m_data; // matrix data

	public:
		// type definitions
		typedef T value_type;
		typedef typename std::vector<T>::iterator iterator;
		typedef typename std::vector<T>::const_iterator const_iterator;

		// container
		iterator begin() { return m_data.begin();  }
		iterator end() { return m_data.end(); }
		const_iterator begin() const { return m_data.begin(); }
		const_iterator end() const { return m_data.end(); }

		// constructors
		matrix() {
			m_dimension.resize(2, 0);
		}
		matrix(const T& v) {
			m_data.push_back(v);
		}
		matrix(int m, int n, const T& v = 0) {
			if (m != 1 || n != 1) m_dimension.push_back(m);
			if (n != 1) m_dimension.push_back(n);
			m_data.resize(m*n, v);
		}
		matrix(const std::vector<int>& d, const T& v = 0) {
			m_dimension = d;
			while (m_dimension.size() && m_dimension.back() == 1)
				m_dimension.pop_back(); // leave true dimension
			m_data.resize(prod(d.begin(),d.end(),int(1)), v);
		}
		matrix(int m, int n, const_iterator it) {
			if (m != 1 || n != 1) m_dimension.push_back(m);
			if (n != 1) m_dimension.push_back(n);
			m_data.assign(it, it + n*m);
		}

		// functions
		template <class S> int sub2ind(const S& s) {
			int i(0), o(1); // index and offset
			for (int k(0); k < (int)m_dimension.size(); ++k) {
				i += o*s[k]; // update index
				o *= m_dimension[k]; // update offset for dimension k
			}
			return i;
		}
		matrix& resize(int n, const T& v=0) {
			m_dimension.clear();
			if (n != 1) m_dimension.push_back(n);
			m_data.resize(n,v);
			return *this;
		}
		matrix& resize(int m, int n, const T& v = 0) {
			m_dimension.clear();
			if (m != 1 || n != 1) m_dimension.push_back(m);
			if (n != 1) m_dimension.push_back(n);
			m_data.resize(m*n, v);
			return *this;
		}
		matrix& resize(const std::vector<int>& d, const T& v = 0) {
			m_dimension= d;
			while (m_dimension.size() && m_dimension.back() == 1)
				m_dimension.pop_back(); // leave true dimension
			m_data.resize(prod(m_dimension.begin(), m_dimension.end(), (int)1), v);
			return *this;
		}
		int size(int d) const {
			if (d > dimension())
				return 1;
			else
				return m_dimension[d-1];
		}
		int dimension() const {
			return (int) m_dimension.size();
		}
		std::vector<int> get_dimension() const {
			return m_dimension;
		}
		int numel() const {
			return (int) m_data.size();
		}
		bool empty() const {
			return numel() == 0;
		}
		template <class P> matrix& append_column_self(const P it) {
			if (dimension() > 2)
				throw std::runtime_error("Operation only applicable to matrices.");
			int n(size(1)), m(size(2));
			m_data.resize(m_data.size() + n);
			std::copy(it, it + n, m_data.end() - n);
			if (m == 0)
				if (n == 1)
					m_dimension.resize(0);
				else
					m_dimension.resize(1);
			else {
				if (m == 1)
					m_dimension.resize(2, 1);
				++m_dimension[1];
			}
			return *this;
		}
		template <class P> matrix append_column(const P it) {
			matrix M(*this);
			M.append_column_self(it);
			return M;
		}
		matrix& pop_column() {
			if (dimension() > 2)
				throw std::runtime_error("Operation only applicable to matrices.");
			if (dimension() <= 1) {
				m_dimension.resize(2, 1);
				m_dimension[1] = 0;
			}
			else {
				if (--m_dimension[1] == 1)
					m_dimension.pop_back();
					if (m_dimension[0] == 1)
						m_dimension.pop_back();
			}
			m_data.resize(m_data.size() - size(1));
			return *this;
		}
		matrix& repeat_self(const std::vector<int>& s) {
			bool b_ones(true);
			std::vector<int>::const_iterator it(s.begin()), ite(--s.end());
			while (it != ite)
				if (*(it++) != 1) {
					b_ones = false;
					break;
				}
			if (b_ones) {
				int n(s.back());
				if (n == 0) {
					m_data.clear();
					m_dimension.resize(s.size(), 1);
					m_dimension.back() = 0;
				}
				else
					if (n > 1) {
						int m(numel());
						m_data.resize(m*n);
						iterator it(begin()), ite(begin() + m), itd(ite);
						for (int i(1); i < n; ++i)
							itd = std::copy(it, ite, itd);
						m_dimension.resize(s.size(), 1);
						m_dimension.back() *= n;
					}
			}
			else
				throw std::runtime_error("TODO: non ending matrix repeat.");
			return *this;
		}
		matrix& repeat_self(int m, int n) {
			std::vector<int> s = {m, n};
			repeat_self(s);
			return *this;
		}
		matrix repeat(const std::vector<int>& s) const {
			matrix M(*this);
			return M.repeat_self(s);
		}
		matrix repeat(int m, int n) const {
			matrix M(*this);
			return M.repeat_self(m, n);
		}
		matrix& cat_self(int d, const matrix& M) {
			// error check
			for (int i(1), dmax(max(dimension(), M.dimension())); i <= dmax; ++i)
				if (i != d && size(i) != M.size(i))
					throw std::runtime_error("Inconsistent matrix dimension.");

			// concatenation
			if (M.empty()) return *this;
			if (dimension() <= d) {
				// append data (fast)
				int sz;
				if (dimension())
					if (M.dimension())
						sz = prod(m_dimension.begin(), m_dimension.end() - 1, (int)1)*(dimension() == d ? m_dimension.back() + M.m_dimension.back() : m_dimension.back()*(1 + M.size(d)));
					else
						sz = 1 + size(d); // cope with scalars
				else
					sz = 1 + M.size(d); // cope with scalars
				m_data.resize(sz);
				std::copy(M.m_data.begin(), M.m_data.begin() + prod(M.m_dimension.begin(), M.m_dimension.end(), (int)1), m_data.begin() + prod(m_dimension.begin(), m_dimension.end(), (int)1));
				m_dimension.resize(d,1);
				m_dimension.back() += M.size(d);
			}
			else {
				// interleave data (slow)
				matrix S(numel() + M.numel(), 1); // temporary matrix
				int step(prod(m_dimension.begin(), m_dimension.begin() + d, (int)1)), stepm(prod(M.m_dimension.begin(), M.m_dimension.begin() + d, (int)1));
				const_iterator it(begin()), itm(M.begin());
				iterator itt(S.begin());
				for (int i(0), imax(prod(m_dimension.begin() + d, m_dimension.end(), (int)1)); i < imax; ++i) {
					itt = std::copy(it, it+step, itt);
					it += step;
					itt = std::copy(itm, itm + stepm, itt);
					itm += stepm;
				}
				S.m_dimension = m_dimension;
				S.m_dimension[d - 1] += M.m_dimension[d - 1];
				*this = S; // update this matrix
			}
			return *this;
		}
		matrix cat(int d, const matrix& M) const {
			matrix C(*this);
			return C.cat_self(d, M);
		}
		matrix& transpose_self() {
			// error check
			if (dimension() > 2)
				throw std::runtime_error("Matrix transpose undefined for dimensions greater than 2.");

			// transposition
			if (dimension() > 0) {
				if (size(1) == 1) {
					std::swap(m_dimension[0], m_dimension[1]);
					m_dimension.pop_back();
				}
				else {
					if (size(2) == 1) {
						m_dimension.push_back(1);
						std::swap(m_dimension[0], m_dimension[1]);
					}
					else
						if (empty())
							std::swap(m_dimension[0], m_dimension[1]);
						else {
							if (m_dimension[0] == 2 && m_dimension[1] == 2) {
								std::swap(m_data[1],m_data[2]);
							}
							else {
								int m(m_dimension[0]), n(m_dimension[1]);
								matrix S(n, m, 0); // temporary transposed matrix
								iterator itt(S.begin());
								for (int i(0); i < m; ++i) {
									const_iterator it(begin() + i);
									*(itt++) = *it;
									for (int j(1); j < n; ++j)
										*(itt++) = *(it += m);
								}
								*this = S; // update matrix to its transposed
							}
					}
				}
			}

			return *this;
		}
		matrix transpose() const {
			matrix C(*this);
			return C.transpose_self();
		}
		matrix& elementwise_product_self(const matrix& M) {
			iterator it(begin()), ite(end());
			const_iterator itm(M.begin());
			while (it != ite)
				*(it++) *= *(itm++);
			return *this;
		}
		matrix elementwise_product(const matrix& M) const {
			matrix P(*this);
			return P.elementwise_product_self(M);
		}
		matrix& elementwise_divide_self(const matrix& M) {
			iterator it(begin()), ite(end());
			const_iterator itm(M.begin());
			while (it != ite)
				*(it++) /= *(itm++);
			return *this;
		}
		matrix elementwise_divide(const matrix& M) const {
			matrix P(*this);
			return P.elementwise_divide_self(M);
		}

		// operators
		const T& operator() (int i) const {
			return m_data[i];
		}
		T& operator() (int i) {
			return m_data[i];
		}
		template <class S> const T& operator() (const S& s) const {
			return m_data[sub2ind(s)];
		}
		template <class S> T& operator() (const S& s) {
			return m_data[sub2ind(s)];
		}
		const T& operator() (int i, int j) const {
			return m_data[i + j*m_dimension[0]];
		}
		T& operator() (int i, int j) {
			return m_data[i + j*m_dimension[0]];
		}
		matrix operator+() const {
			matrix M(*this);
			return M;
		}
		matrix operator-() const {
			matrix M(*this);
			for (iterator it(M.begin()); it != M.end(); ++it)
				*it = -*it;
			return M;
		}
		matrix& operator+=(const T& v) {
			for (iterator it(begin()); it != end(); ++it)
				*it += v;
			return *this;
		}
		matrix& operator+=(const matrix& v) {
			const_iterator itv(v.begin());
			for (iterator it(begin()); it != end(); ++it, ++itv)
				*it += *itv;
			return *this;
		}
		matrix& operator-=(const T& v) {
			for (iterator it(begin()); it != end(); ++it)
				*it -= v;
			return *this;
		}
		matrix& operator-=(const matrix& v) {
			const_iterator itv(v.begin());
			for (iterator it(begin()); it != end(); ++it, ++itv)
				*it -= *itv;
			return *this;
		}
		matrix& operator*=(const T& v) {
			for (iterator it(begin()); it != end(); ++it)
				*it *= v;
			return *this;
		}
		matrix& operator/=(const T& v) {
			for (iterator it(begin()); it != end(); ++it)
				*it /= v;
			return *this;
		}
		matrix operator+(const T& v) const {
			matrix M(*this);
			M += v;
			return M;
		}
		matrix operator+(const matrix& v) const {
			matrix M(*this);
			M += v;
			return M;
		}
		friend matrix operator+(const T& vl, const matrix& vr) {
			matrix M(vr);
			M += vl;
			return M;
		}
		matrix operator-(const T& v) const {
			matrix M(*this);
			M -= v;
			return M;
		}
		matrix operator-(const matrix& v) const {
			matrix M(*this);
			M -= v;
			return M;
		}
		friend matrix operator-(const T& vl, const matrix& vr) {
			matrix M(-vr);
			M += vl;
			return M;
		}
		matrix operator*(const T& v) const {
			matrix M(*this);
			M *= v;
			return M;
		}
		matrix operator*(const matrix& v) const {
			int nlr(size(1)), nlc(size(2));
			int nrr(v.size(1)), nrc(v.size(2));
			matrix M(nlr,nrc,0);
			if (nlc != nrr)
				throw std::runtime_error("Inner matrix dimensions must agree.");
			if (!nlr || !nlc || !nrr || !nrc)
				return M;
			iterator itm(M.begin());
			for (int j(0); j < nrc; ++j) {
				for (int i(0); i < nlr; ++i, ++itm) {
					const_iterator itl(begin()+i);
					const_iterator itr(v.begin()+j*nrr);
					*itm += *itl**itr;
					for (int k(1); k < nlc; ++k)
						*itm += *(itl+=nlr)**(++itr);
				}
			}
			return M;
		}
		friend matrix operator*(const T& vl, const matrix& vr) {
			matrix M(vr);
			M *= vl;
			return M;
		}
		matrix operator/(const T& v) const {
			matrix M(*this);
			M /= v;
			return M;
		}
		friend matrix operator/(const T& vl, const matrix& vr) {
			matrix M(vr.m_dimension);
			const_iterator itv(vr.begin());
			for (iterator it(M.begin()); it != M.end(); ++it, ++itv)
				*it = vl / *itv;
			return M;
		}
		matrix<bool> operator>(const T& v) const {
			matrix<bool> M(m_dimension,false);
			const_iterator itt(begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itt)
				*it = *itt > v;
			return M;
		}
		matrix<bool> operator>(const matrix& v) const {
			matrix<bool> M(m_dimension, false);
			const_iterator itt(begin()), itv(v.begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itt, ++itv)
				*it = *itt > *itv;
			return M;
		}
		friend matrix<bool> operator>(const T& vl, const matrix& vr) {
			matrix<bool> M(vr.m_dimension, false);
			const_iterator itv(vr.begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itv)
				*it = vl > *itv;
			return M;
		}
		matrix<bool> operator<(const T& v) const {
			matrix<bool> M(m_dimension, false);
			const_iterator itt(begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itt)
				*it = *itt < v;
			return M;
		}
		matrix<bool> operator<(const matrix& v) const {
			matrix<bool> M(m_dimension, false);
			const_iterator itt(begin()), itv(v.begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itt, ++itv)
				*it = *itt < *itv;
			return M;
		}
		friend matrix<bool> operator<(const T& vl, const matrix& vr) {
			matrix<bool> M(vr.m_dimension, false);
			const_iterator itv(vr.begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itv)
				*it = vl < *itv;
			return M;
		}
		matrix<bool> operator>=(const T& v) const {
			matrix<bool> M(m_dimension, false);
			const_iterator itt(begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itt)
				*it = *itt >= v;
			return M;
		}
		matrix<bool> operator>=(const matrix& v) const {
			matrix<bool> M(m_dimension, false);
			const_iterator itt(begin()), itv(v.begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itt, ++itv)
				*it = *itt >= *itv;
			return M;
		}
		friend matrix<bool> operator>=(const T& vl, const matrix& vr) {
			matrix<bool> M(vr.m_dimension, false);
			const_iterator itv(vr.begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itv)
				*it = vl >= *itv;
			return M;
		}
		matrix<bool> operator<=(const T& v) const {
			matrix<bool> M(m_dimension, false);
			const_iterator itt(begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itt)
				*it = *itt <= v;
			return M;
		}
		matrix<bool> operator<=(const matrix& v) const {
			matrix<bool> M(m_dimension, false);
			const_iterator itt(begin()), itv(v.begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itt, ++itv)
				*it = *itt <= *itv;
			return M;
		}
		friend matrix<bool> operator<=(const T& vl, const matrix& vr) {
			matrix<bool> M(vr.m_dimension, false);
			const_iterator itv(vr.begin());
			for (matrix<bool>::iterator it(M.begin()); it != M.end(); ++it, ++itv)
				*it = vl <= *itv;
			return M;
		}
	};


	// notable matrices
	template <class T> matrix<T> zeros(int m, int n) {
		return matrix<T>(m, n, 0);
	}
	template <class T> matrix<T> ones(int m, int n) {
		return matrix<T>(m, n, 1);
	}
	template <class T> matrix<T> rand(int m, int n) {
		matrix<T> R(m, n, 0);
		typename matrix<T>::iterator it(R.begin()), ite(R.end());
		while (it != ite)
			*it++ = T(std::rand())/RAND_MAX;
		return R;
	}
	template <class T> matrix<T> eye(int n) {
		matrix<T> I(n, n, 0);
		if (n > 0) {
			typename matrix<T>::iterator it(I.begin());
			*it = 1;
			for (int i(1); i < n; ++i)
				*(it += n + 1) = 1;
		}
		return I;
	}
	template <class T> matrix<T> diag(const matrix<T>& d) {
		int n(d.size(1));
		matrix<T> D(n, n);
		if (n > 0) {
			typename matrix<T>::iterator it(D.begin());
			typename matrix<T>::const_iterator itd(d.begin());
			*it = *itd;
			for (int i(1); i < n; ++i)
				*(it += n + 1) = *(++itd);
		}
		return D;
	}

	// matrix methods
	template <class T> T sum(const T& M, int d = 1) {
		if (M.size(d) == 1)
			return M;
		std::vector<int> dim(M.get_dimension());
		dim[d - 1] = 1;
		T S(dim, 0);
		if (d == 1) {
			typename T::iterator its(S.begin());
			typename T::const_iterator it(M.begin());
			int n(S.numel()), m(M.size(1));
			for (int i(0); i < n; ++i, ++its)
				for (int j(0); j < m; ++j, ++it)
					*its += *it;
		}
		else
			throw std::runtime_error("TODO: sum along dimensions > 1");
		return S;
	}
	template <class T> T max(const matrix<T>& v) {
		T vmax(-inf);
		for (typename matrix<T>::const_iterator it(v.begin()); it != v.end(); ++it)
			if (*it > vmax)
				vmax = *it;
		return vmax;
	}
	template <class T> matrix<T> max(const matrix<T>& x, const matrix<T>& y) {
      matrix<T> vmax(x);
		typename matrix<T>::iterator itmax(vmax.begin());
		for (typename matrix<T>::const_iterator it(y.begin()); it != y.end(); ++it, ++itmax)
			if (*it > *itmax)
				*itmax = *it;
		return vmax;
	}
	template <class T> T min(const matrix<T>& v) {
		T vmin(inf);
		for (typename matrix<T>::const_iterator it(v.begin()); it != v.end(); ++it)
			if (*it < vmin)
				vmin = *it;
		return vmin;
	}
	template <class T> int argmax(const matrix<T>& v) {
		if (v.numel() == 0)
			return -1;
		typename matrix<T>::const_iterator itmax(v.begin());
		for (typename matrix<T>::const_iterator it(v.begin()); it != v.end(); ++it)
			if (*it > *itmax)
				itmax = it;
		return (int)(itmax - v.begin());
	}
	template <class T> matrix<T>& abs_self(matrix<T>& M) {
		typename matrix<T>::iterator it(M.begin()), ite(M.end());
		while (it != ite) {
			*it = fabs(*it);
			++it;
		}
		return M;
	}
	template <class T> matrix<T> abs(const matrix<T>& M) {
		matrix<T> A(M);
		return abs_self(A);
	}
	template <class T> matrix<T>& sqrt_self(matrix<T>& M) {
		typename matrix<T>::iterator it(M.begin()), ite(M.end());
		while (it != ite) {
			*it = sqrt(*it);
			++it;
		}
		return M;
	}
	template <class T> bool all(const matrix<T>& M) {
		for (typename matrix<T>::const_iterator it(M.begin()); it != M.end(); ++it)
			if (!*it)
				return false;
		return true;
	}
	template <class T> bool any(const matrix<T>& M) {
		for (typename matrix<T>::const_iterator it(M.begin()); it != M.end(); ++it)
			if (*it)
				return true;
		return false;
	}
	template <class T> T forward_substitution(const T& A, const T& B) {
		int n(A.size(1)), m(B.size(2));
		T C(n, m, 0);
		for (int i(0); i < n; ++i) {
			typename T::iterator itc(C.begin() + i);
			typename T::const_iterator itb(B.begin() + i);
			for (int j(0); j < m; ) {
				typename T::const_iterator ita(A.begin() + i*n + i);
				*itc = *itb;
				if (i > 0) {
					typename T::const_iterator itaa(A.begin() + i), itcc(C.begin() + j*n);
					for (int k(0); k < i; ++k, itaa += n, ++itcc) {
						*itc -= *itaa * *itcc;
					}
				}
				*itc /= *ita;
				if (++j < m) {
					itb += n;
					itc += n;
				}
			}
		}
		return C;
	}
	template <class T> T backward_substitution(const T& A, const T& B) {
		int n(A.size(1)), m(B.size(2));
		T C(n, m, 0);
		for (int i(n - 1); i >= 0; --i) {
			typename T::iterator itc(C.begin() + i);
			typename T::const_iterator itb(B.begin() + i);
			for (int j(0); j < m; ) {
				typename T::const_iterator ita(A.begin() + i*n + i);
				*itc = *itb;
				if (i < n - 1) {
					typename T::const_iterator itaa(ita), itcc(C.begin() + i + 1 + j*n);
					for (int k(i + 1); k < n; ++k, ++itcc) {
						*itc -= *(itaa += n) * *itcc;
					}
				}
				*itc /= *ita;
				if (++j < m) {
					itb += n;
					itc += n;
				}
			}
		}
		return C;
	}
	template <class T> void gaussian_elimination(T& A, T& B) {
		int ir(0), ic(0); // row and column pivots
		int m(A.size(1)), n(A.size(2)), o(B.size(2)); // matrix size
		while (ir < m && ic < n) {
			// find pivot row
			typename T::iterator itac(A.begin() + ic*m), ita(itac + ir), itaa(ita), itamax(itaa), itae(itac + m);
			typename T::value_type amax(fabs(*itamax)); // maximum value
			while (++itaa != itae) {
				typename T::value_type aa(fabs(*itaa)); // current value
				if (aa > amax) {
					itamax = itaa; // update maximum value iterator
					amax = *itamax; // update maximum value
				}
			}

			// pivot row
			if (amax == 0)
				// skip column
				++ic;
			else {
				// swap pivot row
				typename T::iterator itb;
				if (o > 0)
					itb = B.begin() + ir;
				if (itamax != ita) {
					int dr((int)(itamax - ita));
					itaa = ita;
					itae = A.begin() + m*(n - 1) + ir;
					std::swap(*itaa, *itamax);
					while (itaa != itae)
						std::swap(*(itaa += m), *(itamax += m));
					if (o > 0) {
						typename T::iterator itbb(itb), itbmax(itb + dr), itbe(itb + m*(o - 1));
						std::swap(*itbb, *itbmax);
						while (itbb != itbe)
							std::swap(*(itbb += m), *(itbmax += m));
					}
				}

				// elimination
				for (int i(ir + 1); i < m; ++i) {
					itamax = itac + ir; // pivot row iterator
					itaa = itac + i; // elimination row iterator
					typename T::value_type f(*itaa / *itamax); // row ratio
					*itaa = 0; // fill pivot column with zeros
					for (int j(ic + 1); j < n; ++j)
						*(itaa += m) -= *(itamax += m) * f;
					if (o > 0) {
						typename T::iterator itbb(itb + (i - ir)), itbmax(itb);
						*itbb -= *itbmax * f;
						for (int j(1); j < o; ++j)
							*(itbb += m) -= *(itbmax += m) * f;
					}
				}

				// next pivots
				++ir;
				++ic;
			}
		}
	}
	template <class T> void gauss_jordan_elimination(T& A, T& B, typename T::value_type tol = sqrt(std::numeric_limits<typename T::value_type>::epsilon())) {
		// echelon form
		gaussian_elimination(A, B);

		// reduced echelon form
		int m(A.size(1)), n(A.size(2)), o(B.size(2));
		int ic(0);
		typename T::iterator it(A.begin()), iti, ite(it+m*(n-1));
		for (int ir(0); ir < m; ++ir) {
			// find pivot
			while (*it == 0) {
				if (++ic >= n)
					break;
				it += m;
			}
			if (ic >= n)
				break;

			// put ones on pseudo diagonal
			typename T::value_type f(*it);
			*it = 1;
			iti = it;
			while (iti != ite)
				*(iti += m) /= f;
			if (o > 0) {
				typename T::iterator itbi(B.begin() + ir), itbe(itbi + m*(o - 1));
				*itbi /= f;
				while (itbi != itbe)
					*(itbi += m) /= f;
			}

			// Jordan elimination
			typename T::iterator itsi(it - ir), itii;
			for (int i(0); i < ir; ++i) {
				iti = it;
				itii = itsi;
				if (fabs(*itii) > tol) {
					f = *itii;
					*itii = 0;
					while (iti != ite)
						(*(itii += m) /= f) -= *(iti += m);
					if (o > 0) {
						typename T::iterator itbi(B.begin() + i), itbe(itbi + m*(o - 1)), itb(B.begin() + ir);
						(*itbi /= f) -= *itb;
						while (itbi != itbe)
							(*(itbi += m) /= f) -= *(itb += m);
					}
				}
				else
					*itii = 0;
				++itsi;
			}

			// next row
			++it;
			++ite;
		}
	}
	template <class T> void scale_columns(T& A, const T& s) {
		int m(A.size(1)), n(A.size(2));
		typename T::iterator it(A.begin());
		typename T::const_iterator its(s.begin());
		for (int i(0); i < n; ++i, ++its) {
			for (int j(0); j < m; ++j, ++it)
				*it *= *its;
		}
	}
	template <class T> void unit_columns(T& A) {
		int m(A.size(1)), n(A.size(2));
		typename T::iterator it(A.begin());
		for (int i(0); i < n; ++i) {
			typename T::value_type s(0);
			for (int j(0); j < m; ++j, ++it)
				s += *it * *it;
			s = sqrt(s);
			it -= m;
			for (int j(0); j < m; ++j, ++it)
				*it /= s;
		}
	}
	template <class T, class B> T select_columns(const T& A, const B& b) {
		int n(A.size(1));
		T M(n, 0);
		typename T::const_iterator ita(A.begin());
		for (typename B::const_iterator itb(b.begin()); itb != b.end(); ++itb, ita += n)
			if (*itb)
				M.append_column_self(ita);
		return M;
	}
	template <class T> T select_column(const T& A, int ic) {
		int n(A.size(1)); // number of rows
		return T(n, 1, A.begin() + n*ic);
	}
	template <class T> typename T::value_type det_abs(const T& A) {
		int n(A.size(1)), m(A.size(2));
		if (n != m)
			throw std::runtime_error("Matrix must be square");
		if (n == 0)
			return 0;
		if (n == 1)
			return fabs(A(0));
		if (n == 2)
			return fabs(A(0)*A(3) - A(1)*A(2));
		T M(A), B(n, 0);
		gaussian_elimination(M, B);
		typename T::const_iterator it(M.begin()), ite(--M.end());
		typename T::value_type D(*it);
		while (it != ite)
			D *= *(it += n + 1);
		return fabs(D);
	}
	template <class T> T gram_schmidt_orthogonalization(const T& A) {
		T B(A.transpose()), M(B*A);
		gaussian_elimination(M, B);
		B.transpose_self();
		unit_columns(B);
		return B;
	}
	template <class T> T cholesky_decomposition(const T& A) {
		int m(A.size(1)), n(A.size(2));
		if (n != m)
			throw std::runtime_error("Matrix must be square.");
		T L(n, n, 0);
		for (int i(0); i < n; ++i) {
			typename T::iterator it(L.begin() + i), itk(it);
			typename T::const_iterator ita(A.begin() + i);
			for (int j(0); j < i; ++j, it += n, ita += n) {
				*it = *ita;
				typename T::iterator iti(L.begin() + i), itj(L.begin() + j);
				for (int k(0); k < j; ++k, iti += n, itj += n)
					*it -= *iti * *itj;
				*it /= *itj;
			}
			*it = *ita;
			for (int k(0); k < i; ++k, itk += n) {
				*it -= *itk * *itk;
			}
			if (*it < 0)
				throw std::runtime_error("Matrix must be symmetric positive-definite.");
			*it = sqrt(*it);
		}
		return L;
	}
	template <class T> T solve(const T& A, const T& B) {
		T U(A), V(B);
		gaussian_elimination(U, V);
		return backward_substitution(U, V);
	}
	template <class T> T null(const T& A, typename T::value_type tol = sqrt(std::numeric_limits<typename T::value_type>::epsilon())) {
		int m(A.size(1)), n(A.size(2));
		T B(A.transpose()), M(eye<typename T::value_type>(n)), N(n, 0);
		if (m == 0)
			return M;
		gauss_jordan_elimination(B, M, tol);
		B.transpose_self();
		M.transpose_self();
		typename T::iterator itm(M.end()), itb(B.end());
		for (int i(0); i < n;  ++i) {
			itm -= n;
			itb -= m;
			T b(m, 1, itb);
			if (!any(b))
				N.cat_self(2, T(n, 1, itm));
			else
				break;
		}
		return gram_schmidt_orthogonalization(N);
	}

}



#endif