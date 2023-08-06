.. _picos_for_qis:

.. role:: pyth(code)
   :language: python

PICOS for Quantum Information Science
=====================================

PICOS was among the first convex optimization interfaces to natively support
Hermitian semidefinite programming and subsystem manipulation operations such as
the partial trace and partial transpose, which were implemented with feedback
from the QIS community. This note outlines the features most relevant for the
field and links to examples.


QIS Cheat Sheet
---------------


.. list-table:: Complex expression manipulation
  :header-rows: 1

  * - on paper
    - in picos

  * - :math:`A \in \mathbb{C}^{m \times n}`
    - :pyth:`A = pc.ComplexVariable("A", (m, n))`

  * - :math:`A = B + iC`
    - :pyth:`A = B + 1j*C`

  * - :math:`\Re(A)`
    - :pyth:`A.real`

  * - :math:`\Im(A)`
    - :pyth:`A.imag`

  * - :math:`\overline{A}`
    - :pyth:`A.conj`

  * - :math:`A^\dagger`
    - :pyth:`A.H`

  * - :math:`\frac{1}{2} \left( A^\dagger + A \right)`
    - :pyth:`A.hermitianized`

  * - :math:`\langle \psi \vert \psi \rangle`
    - :pyth:`psi.H * psi`

  * - :math:`\rvert \psi \rangle \langle \psi \lvert`
    - :pyth:`psi * psi.H`


.. list-table:: Hermitian semidefinite programming
  :header-rows: 1

  * - on paper
    - in picos

  * - :math:`\rho \in \mathbb{S}^n`
    - :pyth:`rho = pc.HermitianVariable("ρ", n)`

  * - :math:`\rho \succeq 0`
    - :pyth:`rho >> 0`

  * - :math:`\rho \succeq I`
    - :pyth:`rho >> 1` / :pyth:`rho >> pc.I(n)`

  * - :math:`\operatorname{Tr}(\rho) = 1`
    - :pyth:`rho.tr == 1`

  * - :math:`\begin{bmatrix}A & B \\ C & D\end{bmatrix} \succeq 0`
    - :pyth:`pc.block([[A, B], [C, D]]) >> 0`


.. list-table:: Schatten norms
  :header-rows: 1

  * - on paper
    - in picos
    - note / aka

  * - :math:`{\lVert A \rVert}_1 = \operatorname{Tr}\left( \sqrt{A^\dagger A} \right)`
    - :pyth:`pc.NuclearNorm(A)`
    - *trace norm*

  * - :math:`{\lVert A \rVert}_\infty = \sqrt{\lambda_{\max}(A^\dagger A)}`
    - :pyth:`pc.SpectralNorm(A)`
    - :math:`\lambda_{\max}(A)` for :math:`A \in \mathbb{H}^n`


.. list-table:: Subsystem manipulation (partial trace, partial transpose, realignment)
  :header-rows: 1

  * - on paper
    - in picos
    - note / docs

  * - :math:`A = B \otimes C`
    - :pyth:`A = B @ C`
    -

  * - :math:`A_1 \otimes \cdots \otimes \operatorname{Tr}(A_i) \otimes \cdots \otimes A_n`
    - :pyth:`A.partial_trace([i-1], shapes)`
    - :meth:`~picos.expressions.exp_biaffine.BiaffineExpression.partial_trace`

  * - :math:`A_1 \otimes \cdots \otimes A_i^T \otimes \cdots \otimes A_n`
    - :pyth:`A.partial_tranpose([i-1], shapes)`
    - :meth:`~picos.expressions.exp_biaffine.BiaffineExpression.partial_transpose`

  * - :math:`A_{ij\;\mapsto\;ji} = A^T`
    - :pyth:`A.reshuffled("ji")`
    - :meth:`~picos.expressions.exp_biaffine.BiaffineExpression.reshuffled`

  * - :math:`A_{ijkl\;\mapsto\;kjil} = \operatorname{T}_1(A)`
    - :pyth:`A.reshuffled("kjil")`
    - :meth:`~picos.expressions.exp_biaffine.BiaffineExpression.reshuffled`

  * - :math:`\operatorname{Tr}_1(A),\;\ldots{},\;\operatorname{Tr}_4(A),\;\operatorname{Tr}_\text{last}(A)`
    - :pyth:`A.tr0`, ..., :pyth:`A.tr3`, :pyth:`A.trl`
    - :math:`A \in \mathbb{H}^2 \otimes \cdots \otimes \mathbb{H}^2`

  * - :math:`\operatorname{T}_1(A),\;\ldots{},\;\operatorname{T}_4(A),\;\operatorname{T}_\text{last}(A)`
    - :pyth:`A.T0`, ..., :pyth:`A.T3`, :pyth:`A.Tl`
    - :math:`A \in \mathbb{H}^2 \otimes \cdots \otimes \mathbb{H}^2`

(:math:`\operatorname{Tr}_i` and :math:`\operatorname{T}_i` denote the partial
trace and transpose of the :math:`i`-th :math:`2 \times 2` subsystem, counted
from zero)


Hermitian semidefinite programming
----------------------------------

PICOS makes use of the following identity to allow standard solvers to deal with
hermitian LMIs:

.. math::

  A \succeq 0
  \qquad
  \Longleftrightarrow
  \qquad
  \begin{bmatrix}
    \Re(A) & \Im(A) \\
    -\Im(A) & \Re(A)
  \end{bmatrix} \succeq 0

Hermitian variables are vectorized such that :math:`\rho \in \mathbb{S}^n` is
passed to solvers via :math:`n^2` real scalar variables.


Examples and exercises
----------------------

  - :ref:`Fidelity between operators <fidelity>`
  - `Quantum channel discrimination
    <https://mybinder.org/v2/gl/picos-api%2Fmadrid23/HEAD?urlpath=tree/04_complex_sdps.ipynb>`__
    (exercise on Binder)


Recent research using PICOS
---------------------------

2023
~~~~

- Felix Huber and Nikolai Wyderka.
  **Refuting spectral compatibility of quantum marginals.**
  *arXiv preprint*, v2, 2023.
  arXiv: `2211.06349 <https://arxiv.org/abs/2211.06349>`__.
- Aby Philip, Soorya Rethinasamy, Vincent Russo, and Mark M. Wilde.
  **Quantum Steering Algorithm for Estimating Fidelity of Separability.**
  *arXiv preprint*, 2023.
  arXiv: `2303.07911 <https://arxiv.org/abs/2303.07911>`__.
  code: `on arxiv.org <https://arxiv.org/src/2303.07911/anc>`__.

2022
~~~~

- Armin Tavakoli, Alejandro Pozas-Kerstjens, Ming-Xing Luo, and Marc-Olivier Renou.
  **Bell nonlocality in networks.**
  *Reports on Progress in Physics*, 85, 2022.
  arXiv: `2104.10700 <https://arxiv.org/abs/2104.10700>`__.
  DOI: `10.1088/1361-6633/ac41bb <https://doi.org/10.1088/1361-6633/ac41bb>`__.
- Feng-Jui Chan et al.
  **Maxwell’s two-demon engine under pure dephasing noise.**
  *Physical Review A*, 106, 2022.
  arXiv: `2206.05921 <https://arxiv.org/abs/2206.05921>`__.
  DOI: `10.1103/PhysRevA.106.052201
  <https://doi.org/10.1103/PhysRevA.106.052201>`__.
- Viktor Nordgren et al.
  **Certifying emergent genuine multipartite entanglement with a partially blind witness.**
  *Physical Review A*, 106, 2022.
  preprint: `on st-andrews.ac.uk
  <https://research-repository.st-andrews.ac.uk/bitstream/10023/26655/1/Nordgren_2022_PRA_Certifying_emergent_VoR.pdf>`__.
  DOI: `10.1103/PhysRevA.106.062410
  <https://doi.org/10.1103/PhysRevA.106.062410>`__
- Matthew DeCross, Eli Chertkov, Megan Kohagen, and Michael Foss-Feig.
  **Qubit-reuse compilation with mid-circuit measurement and reset.**
  *arXiv preprint*, 2022.
  arXiv: `2210.08039 <https://arxiv.org/abs/2210.08039>`__.
- Vincent Russo and Jamie Sikora.
  **A note on the inner products of pure states and their antidistinguishability.**
  *arXiv preprint*, 2022.
  arXiv: `2206.08313 <https://arxiv.org/abs/2206.08313>`__.
  code: `on github.com <https://github.com/vprusso/antidist>`__.
- Sarnava Datta, Hermann Kampermann, and Dagmar Bruß.
  **Upper bound on the Guessing probability using Machine Learning.**
  *arXiv preprint*, 2022.
  arXiv: `2212.08500 <https://arxiv.org/abs/2212.08500>`__.

2021
~~~~

- Ulysse Chabaud, Pierre-Emmanuel Emeriau, and Frédéric Grosshans.
  **Witnessing Wigner Negativity.**
  *Quantum*, 5(471), 2021.
  arXiv: `2102.06193 <https://arxiv.org/abs/2102.06193>`__.
  DOI: `10.22331/q-2021-06-08-471 <https://doi.org/10.22331/q-2021-06-08-471>`__.
  code:
  `on softwareheritage.org
  <https://archive.softwareheritage.org/browse/directory/d98f70e386783ef69bf8c2ecafdb7b328b19b7ec/>`__.
- Pierre-Emmanuel Emeriau.
  **The interplay between quantum contextuality and Wigner negativity.**
  PhD thesis, 2021.
  arXiv: `2204.08782 <https://arxiv.org/abs/2204.08782>`__.

(list updated 2023-03)


Connection with Ncpol2sdpa
--------------------------

`Ncpol2sdpa <https://ncpol2sdpa.readthedocs.io/en/stable/index.html>`_ [:ref:`1
<picos_for_qis_refs>`] exposes SDP relaxations of (non-commutative) polynomial
optimization problems as PICOS problem instances, see `here
<https://ncpol2sdpa.readthedocs.io/en/stable/exampleshtml.html#example-5-additional-manipulation-of-the-generated-sdps-with-picos>`__.


Course material
---------------

Jupyter notebooks for a hands-on workshop on practical semidefinite programming
aimed at quantum information students are available `on GitLab
<https://gitlab.com/picos-api/madrid23>`__. The fourth notebook is based on
[:ref:`2 <picos_for_qis_refs>`], which also comes with Python/PICOS `notebooks
<https://github.com/vsiddhu/SDP-Quantum-OR>`__.


.. _picos_for_qis_refs:

References
----------

  1. Peter Wittek.
     Algorithm 950: Ncpol2sdpa—sparse semidefinite programming relaxations for
     polynomial optimization problems of noncommuting Variables.
     *ACM Transactions on Mathematical Software*, 41(3), 21, 2015.
     DOI: `10.1145/2699464 <dx.doi.org/10.1145/2699464>`__.
     arXiv: `1308.6029 <http://arxiv.org/abs/1308.6029>`__.
  2. Vikesh Siddhu and Sridhar Tayur.
     Five starter pieces: quantum information science via semi-definite programs.
     *INFORMS TutORials in Operations Research*, 2022.
     DOI: `10.1287/educ.2022.0243 <https://doi.org/10.1287/educ.2022.0243>`__.
     arXiv: `2112.08276 <https://arxiv.org/abs/2112.08276>`__.
