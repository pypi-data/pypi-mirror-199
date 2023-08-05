#ifndef _ALGORITHMS_H_
#define _ALGORITHMS_H_

#include <vector>
#include <cmath>

#include "matrix.h"

namespace dopt {

	// Golden section algorithm: univariate optimization algorithm.
	template <class T, class E> T golden_section(E f, T a, T b, T epsilon, int n_max = 200) {
		const T Phi = ((T)sqrt(5.0) - 1) / 2; // golden ratio
		T dx(b - a), alpha[4] = { a, b - Phi*dx, a + Phi*dx, b }, delta(b-a); // sample points
		std::pair<matrix<T>, matrix<T> > fab(f(matrix<T>(a)), f(matrix<T>(b))), falpha(f(matrix<T>(alpha[1])), f(matrix<T>(alpha[2]))); // function values
		int k = 0;
		while ((delta > epsilon*dx) && k < n_max) { // stop criterion: uncertainty
			if (all(falpha.first <= falpha.second) || all(-max(-falpha.first, -falpha.second) >= fab.first)) {
			    // remove last interval
			    delta = alpha[2] - alpha[0];
				alpha[3] = alpha[2];
				alpha[2] = alpha[1];
				alpha[1] = alpha[3] - Phi*delta;
				falpha.second = falpha.first;
				falpha.first = f(matrix<T>(alpha[1]));
			}
			else {
				// remove first interval
				delta = alpha[3] - alpha[1];
				alpha[0] = alpha[1];
				alpha[1] = alpha[2];
				alpha[2] = alpha[0] + Phi*delta;
				falpha.first = falpha.second;
				falpha.second = f(matrix<T>(alpha[2]));
			}
			k += 1;
		}
		return (alpha[1] + alpha[2]) / 2;
	}

	// multiple cuts: apply multiple cuts to ellipsoid.
	template <class M> bool apply_multiple_cuts(M& xk, M& Qik, M& Mk, M& D, M& X, const M& Di, const M& Xi, typename M::value_type Vmax, int& stop, typename M::value_type shallowcut = 0, bool decomposition = true, bool memory = true, int kmax = 32) {
		// types
		typedef typename M::value_type T;
		typedef typename M::iterator iterator;
		typedef typename M::const_iterator const_iterator;

		// constants
		const int n(X.size(1));

		// memory
		std::vector<bool> temporary(D.size(2), false); // temporary cut indicator
		D.cat_self(2, Di); X.cat_self(2, Xi); // append new cuts
		if (memory)
			temporary.resize(D.size(2), false);
		else
			temporary.resize(D.size(2), true);

		// cuts
		M Delta, Alpha, Dk;
		for (int k(0); k < kmax; ++k) {
			// normalization factors
			Delta = Qik*D;
			Delta.elementwise_product_self(D);
			Delta = sum(Delta, 1);
			if (any(Delta <= 1e-200)) { // stop criterion: degenerate ellipsoid
				stop = 3; // stop by degenerate ellipsoid
				return true;
			}

			// cut directions
			int nc(D.size(2)); // number of cuts
			Dk = D;
			iterator it(Dk.begin());
			const_iterator itd(Delta.begin());
			for (int ic(0); ic < nc; ++ic, ++itd) {
				T f(1 / sqrt(*itd));
				for (int i(0); i < n; ++i, ++it)
					*it *= f; // column scale
			}

			// cut depths
			Alpha = X;
			iterator ita(Alpha.begin());
			for (int ic(0); ic < nc; ++ic) {
				const_iterator itx(xk.begin());
				for (int i(0); i < n; ++i, ++ita, ++itx)
					*ita -= *itx; // column offset
			}
			Alpha.elementwise_product_self(Dk);
			Alpha = sum(Alpha, 1);

			// choose cut
			int ialpha(argmax(Alpha));
			T alpha(Alpha(ialpha)), ck(Delta(ialpha));
			if (alpha > 1) { // stop criteria: degenerate ellipsoid
				stop = 2; // stop by empty localizing set
				return true;
			}
			if (alpha < -shallowcut / n) // stop criteria: cut is not enough deep
				break;
			M dk(Qik*select_column(Dk, ialpha)), dpk(Mk*select_column(D, ialpha));

			// update ellipsoid
			T tau((1 + n*alpha) / (n + 1)), delta((n*n)*(1 - alpha*alpha) / (n*n - 1)), sigma(2 * (1 + n*alpha) / (n + 1) / (1 + alpha)), pi(1 + sqrt(1 - sigma));
			xk += tau*dk; // update ellipsoid center
			if (decomposition) {
				Mk = sqrt(delta)*(eye<T>(n) - pi / ck*(dpk*dpk.transpose()))*Mk; // update ellipsoid matrix
				Qik = Mk.transpose()*Mk; // update ellipsoid matrix
			}
			else
				Qik = delta*(Qik - sigma*(dk*dk.transpose()));

			// prune cuts
			for (int i(0); i < nc; )
				if (Alpha(i) <= -1) {
					Alpha(i) = Alpha(--nc);
					temporary[i] = temporary[nc];
					{
						iterator itx(D.begin() + i*n), itdx(D.begin() + nc*n);
						std::copy(itdx, itdx + n, itx);
					}
					D.pop_column();
					{
						iterator itx(X.begin() + i*n), itdx(X.begin() + nc*n);
						std::copy(itdx, itdx + n, itx);
					}
					X.pop_column();
				}
				else
					++i;
		}

		// prune memory
		if (!memory) {
			int nc(D.size(2)); // number of cuts
			for (int i(0); i < nc; )
				if (temporary[i]) {
					temporary[i] = temporary[--nc];
					{
						iterator itx(D.begin() + i*n), itdx(D.begin() + nc*n);
						std::copy(itdx, itdx + n, itx);
					}
					D.pop_column();
					{
						iterator itx(X.begin() + i*n), itdx(X.begin() + nc*n);
						std::copy(itdx, itdx + n, itx);
					}
					X.pop_column();
				}
				else
					++i;
		}

		// stop criterion
		if (Vmax > 0 && sqrt(det_abs(Qik)) <= Vmax) { // stop criterion: content reduction
			stop = 1; // stop by volume reduction
			return true;
		}
		return false;
	}

	// ellipsoid method: multivariate optimization algorithm.
	template <class M, class EF, class EDF, class EG, class EDG> std::pair<M, M> ellipsoid(EF f, EDF df, EG g, EDG dg, const M& A, const M& b, const M& Aeq, const M& beq, const M& xmin, const M& xmax, M& x, M&Fx, M& Qi, int& stop, typename M::value_type epsilon = 0, int kmax = 300, int kimax = 32, typename M::value_type shallowcut = 0, bool decomposition = true, bool memory = true, bool log = false) {
		// types
		typedef typename M::value_type T;

		// constants
		const int n(xmin.size(1));

		// starting point
		if (x.empty())
			x = (xmin + xmax) / 2;

		// linear equality constraints
		M R(null(Aeq)), Rt(R.transpose()), Ar(Aeq.cat(1, R.transpose())), Art(Ar.transpose()), br(beq.cat(1, M(R.size(2), 1, 0))), r(solve(Art*Ar, Art*br)); // linear transformatoin for nullspace

		// starting ellipsoid
		M xk(Rt*(x - r)); // center
		M Mk, Qik; // matrix square root
		if (Qi.empty()) {
			Mk = diag(sqrt(n)*max(xmax - x, x - xmin))*R;
			Qik = Mk.transpose()*Mk; // matrix
		}
		else
			if (Qi.size(1) == n)
				Qik = Rt*Qi*R; // project ellipsoid on linear equality constraints
		Qi = Qik; // starting matrix
		Mk = cholesky_decomposition(Qik).transpose_self(); // matrix square root

		// cut history
		M D(R.size(2), 0), X(R.size(2), 0); // directions and points

		// bounds and linear inequality constraints
		M Au(A.transpose()), bu(b); // linear inequality constraints
		Au.cat_self(2, eye<T>(n)).cat_self(2, -eye<T>(n)); bu.cat_self(1, xmax).cat_self(1, -xmin); // bounds
		bu -= Au.transpose()*r; Au = Rt*Au; // projection on null space
		M an(Au); an.elementwise_product_self(an); an = sum(an, 1); sqrt_self(an); // inequality norms
		scale_columns(Au, 1 / an); bu.elementwise_divide_self(an); // unit normals
		M Xa(Au); scale_columns(Xa, bu); // point on constraints
		D.cat_self(2, -select_columns(Au, an > 0));
		X.cat_self(2, select_columns(Xa, an > 0));

		// best so far
		M fx, gx; // function evaluation
		M yb(n, 0), fxb(0, 0), fyb(0, 0), yk(R*xk + r); // best so far
		if (all((A*yk - b) <= 0) && all((yk - xmax) <= 0) && all((xmin - yk) <= 0) && all(g(yk) <= 0)) {
			fx = f(yk);
			fxb = fx;
			fyb = fx;
			yb = yk;
		}

		// iterations
		M dk, dpk; // temporary
		epsilon = pow(epsilon, n); // uncertainty to each variable
		T Vmax(sqrt(det_abs(Qik))*epsilon); // stopping maximum volume
		stop = 0; // default stop: maximum number of iterations
		if (!apply_multiple_cuts(xk, Qik, Mk, D, X, M(D.size(1), 0), M(X.size(1), 0), Vmax, stop, shallowcut, decomposition, memory, kimax)) {
			for (int k(0); k < kmax; ++k) {
				// function evaluation
				yk = R*xk + r; // original space
				fx = f(yk); // evaluate objective functions
				gx = g(yk); // evaluate constraint functions
				
				// initialization
				if (k == 0) {
					if (fxb.empty()) fxb.resize(fx.size(1), 1, inf);
					fyb.resize(fx.size(1), 0);
				}

				// cuts
				gx.cat_self(1, fx - fxb); // append dominance constraint
				matrix<bool> bgx(gx > 0); // violated contraint indicator
				if (any(bgx) || any((A*yk - b) > 0) || any((yk - xmax) > 0) || any((xmin - yk) > 0))
					dk = -select_columns((dg(yk).cat_self(2, df(yk))), bgx); // cuts from constraint
				else {
					if (log) {
						yb.cat_self(2, yk); // append best so far
						fyb.cat_self(2, fx); // append best so far
					}
					else {
						yb = yk; // update best so far
						fyb = fx; // update best so far
					}
					fxb = fx; // update best so far
					dk = -df(yk); // cuts from objective
				}

				// log of information
				if (log && !Fx.empty()) {
					x.cat_self(2, yk); // append
					Fx.cat_self(2, fx); // append
					Qi.cat_self(3, Qik); // append
				}
				else {
					x = yk; // update
					Fx = fx; // update
					Qi = Qik;// update
				}

				// apply multiple cuts
				if (apply_multiple_cuts(xk, Qik, Mk, D, X, Rt*dk, xk.repeat(1, dk.size(2)), Vmax, stop, shallowcut, decomposition, memory, kimax))
					break;
			}
		}
		
		// update best so far
		yk = R*xk + r; // original space
		fx = f(yk); // evaluate objective functions
		if (all(yk >= xmin) && all(yk <= xmax) && all(A*yk <= b)) {
			if (fxb.empty())
				fxb = M(fx.size(1), 1, inf);
			gx = g(yk); // evaluate constraint functions
			gx.cat_self(1, fx - fxb); // append dominance constraint
			if (all(gx <= 0)) {
				if (log && !fyb.empty()) {
					yb.cat_self(2, yk); // append best so far
					fyb.cat_self(2, fx); // append best so far
				}
				else {
					yb = yk; // update best so far
					fyb = fx; // update best so far
				}
			}
		}
		
		// log of information
		if (log && !Fx.empty()) {
			x.cat_self(2, yk); // append
			Fx.cat_self(2, fx); // append
			Qi.cat_self(3, Qik); // append
		}
		else {
			x = yk; // update
			Fx = fx; // update
			Qi = Qik;// update
		}

		return std::pair<M, M>(yb, fyb);
	}
}


#endif