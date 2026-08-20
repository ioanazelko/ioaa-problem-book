1.22 OK
1.23 OK
1.24 OK
1.25 FIXED-PROPOSED: add sic for official error (Altair RV -26.9 in solution vs -26.1 in problem table; tangential terms appear computed with Vega's distance)
OLD<<<  \[ v_1 = (-13.9, 7.33, 10.45)\quad\text{and}\quad
     v_2 = (-26.9, 19.57, 14.06) \]
  \hfill(4 points)>>>
NEW<<<  \[ v_1 = (-13.9, 7.33, 10.45)\quad\text{and}\quad
     v_2 = (-26.9, 19.57, 14.06) \]
  % sic: source uses radial velocity -26.9 for Altair though the problem
  % table gives -26.1; Altair's tangential components also appear to be
  % computed with Vega's distance (7.6787 pc) rather than Altair's
  \hfill(4 points)>>>
1.26 OK
1.27 OK
1.28 FLAG: official solution includes a small geometry diagram (T, H, D, R_earth, C, T'); book solution has no \ioaafig and no 2018_TH_T4 solution figure exists in images/ -- text is complete, but figure omission may be intentional or an oversight
1.29 OK
1.30 OK
1.31 OK
1.32 OK
1.33 OK
1.34 OK
1.35 OK
1.36 OK
1.37 OK
1.38 OK
1.39 FIXED-PROPOSED: add sic for official typo in cosine-rule expansion (first RHS term should be -sin(a)sin(phi); official prints -sin(a)cos(phi); harmless since a=0)
OLD<<<    \therefore -\sin(\delta)
      &= -\sin(a)\cos(\phi) - \cos(a)\cos(\phi)\cos(A)
  \end{align*}>>>
NEW<<<    \therefore -\sin(\delta)
      &= -\sin(a)\cos(\phi) - \cos(a)\cos(\phi)\cos(A)
      % sic: the official solution writes -sin(a)cos(phi) for the first term;
      % expanding the law of cosines gives -sin(a)sin(phi). The term vanishes
      % anyway since a = 0 at sunrise.
  \end{align*}>>>
1.40 OK
1.41 OK
1.42 OK (note: official paper misspells "Triffid Nebula"; book uses correct "Trifid" silently -- left as is)
