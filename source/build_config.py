#!/usr/bin/env python
"""Generate split configs for all IOAA problem & solution PDFs."""
import json, re

J = []

def job(file, problems, **kw):
    J.append(dict(file=file, problems=problems, **kw))

def P(pid, rx=None, **kw):
    d = dict(id=pid)
    if rx: d["rx"] = rx
    d.update(kw)
    return d

# ---------------- PROBLEM PAPERS ----------------

# 2007 theory: shorts 1.1-1.15 (text ok), longs pages 5-7 (garbled font) 0-based 4-6
job("2007_th.pdf",
    [P(f"2007_TH_1.{i}", rf"^1\.{i}\b") for i in range(1, 16)] +
    [P("2007_TH_Q2", pages=[2, 2]), P("2007_TH_Q3", pages=[3, 3]), P("2007_TH_Q4", pages=[4, 6])])

job("2007_da.pdf", [P(f"2007_DA_D{i}", rf"^Question {i}\b") for i in (1, 2, 3)])

w8 = ["Two persons, on the equator", "On April 2, 2008 a telescope", "A full moon occurred",
      "Suppose a star has a mass", "The average temperature of the Cosmic",
      "Radio wavelength observations", "A main sequence star at a distance",
      "Gravitational forces of the Sun", "The radiation incoming to the Earth",
      "The coordinates of the components", "Below is a picture on a 35 mm",
      "Consider a type Ia supernova", "In the journey of a space", "Consider a Potentially Hazardous",
      "Galaxy NGC 2639"]
job("2008_th.pdf",
    [P(f"2008_TH_S{i+1}", rf"^{i+1}\.\s*{re.escape(w[:18])}") for i, w in enumerate(w8)] +
    [P("2008_TH_L1", r"^An eclipsing binary star system"),
     P("2008_TH_L2", r"^2\.?\s*A UBV photometric"),
     P("2008_TH_L3", r"^3\.?\s*Measurement of the cosmic microwave")])

job("2008_da.pdf", [P("2008_DA_D1", r"^I\.\s*Virgo Cluster"),
                    P("2008_DA_D2", r"^II\.\s*Determination of stellar"),
                    P("2008_DA_D3", r"^III\.\s*The Age of Meteorite")])

job("2009_th.pdf", [P(f"2009_TH_P{i}", rf"^Problem {i}\s*:") for i in range(1, 18)])
job("2009_da.pdf", [P("2009_DA_D1", r"^Problem\s+1\s*:"), P("2009_DA_D2", r"^Problem\s+2\s*:")])

w10 = ["In a binary system", "If the escape velocity", "The observed redshift of a QSO",
       "A binary system is 10 pc", "If 0.8% of the initial", "A spacecraft landed",
       "We are interested in finding", "The Galactic Center is believed",
       "A star has a measured I-band", "Assuming that the G-type", "Mars arrived at its great",
       "The difference in brightness", "Estimate the effective temperature",
       "An observer observed a transit", "On average, the visual diameter"]
# 2010: problems live inside the solutions file; statement = anchor -> "Solution"
job("2010_th_sol.pdf",
    [P(f"2010_TH_S{i+1}", rf"^{i+1}\)\s*{re.escape(w[:16])}", stop_rx=r"^Solution") for i, w in enumerate(w10)] +
    [P("2010_TH_L16", r"^16\)\s*A spacecraft is launched", stop_rx=r"^Solution"),
     P("2010_TH_L17", r"^17\)\s*The planet Taris", stop_rx=r"^Solution")])
# full spans for the solutions part
job("2010_th_sol.pdf",
    [P(f"2010_THSOL_S{i+1}", rf"^{i+1}\)\s*{re.escape(w[:16])}") for i, w in enumerate(w10)] +
    [P("2010_THSOL_L16", r"^16\)\s*A spacecraft is launched"),
     P("2010_THSOL_L17", r"^17\)\s*The planet Taris")])

job("2010_da.pdf", [P("2010_DA_D1", r"^Problem I\b.*CCD"), P("2010_DA_D2", r"^Problem II\s*:")])

w11 = ["Most single-appearance comets", "Estimate the number of stars in a globular",
       "On 9 March 2011 the Voyager", "Assuming that Phobos moves", "What would be the diameter of a radio",
       "Tidal forces result in a torque", "A satellite orbits the Earth on a circular",
       "Assuming that dust grains are black", "Interstellar distances are large",
       "Estimate the minimum energy a proton", "Based on the spectrum of a galaxy",
       "Due to the precession of the Earth", "The equation of the ecliptic",
       "Estimate the number of solar neutrinos", "Given that the cosmic background"]
job("2011_th.pdf",
    [P(f"2011_TH_S{i+1}", rf"^{i+1}\.\s*{re.escape(w[:16])}",
       **({"stop_rx": r"^Astronomical and physical constants"} if i == 14 else {})) for i, w in enumerate(w11)] +
    [P("2011_TH_L1", r"^A transit of duration"),
     P("2011_TH_L2", r"^Within the field of a galaxy cluster"),
     P("2011_TH_L3", r"^The planetarium program")])

job("2011_da.pdf", [P("2011_DA_D1", r"^Analysis of times of minima$"),
                    P("2011_DA_D2", r"^Weighing a galaxy$")])

w12 = ["At Brazil", "Calculate the length of the sidereal", "What is the time interval between",
       "What would be full Moon", "Calculate the ratio between the average",
       "Most of the energy emitted by the Sun", "Luminous Blue Variable",
       "A pulsar located 1000 pc", "An old planetary nebula", "Assume that the universe currently",
       "What is the angular amplitude", "What is the minimum diameter of a telescope",
       "An astronomer in the southern hemisphere", "An observer in Salonika",
       "Christ, the Redeemer"]
job("2012_th.pdf",
    [P(f"2012_TH_S{i+1}", rf"^{i+1}\.\s*{re.escape(w[:16])}") for i, w in enumerate(w12)] +
    [P("2012_TH_L1", r"^1\.\s*An astronomer on Earth observes a globular"),
     P("2012_TH_L2", r"^2\.\s*Astronomers studied a spiral galaxy")])

job("2012_da.pdf", [P("2012_DA_D1", r"^Question 1\b"), P("2012_DA_D2", r"^Question 2\b")])

w13 = ["What would be the mean temperature", "Let us assume that we observe a hot",
       "It is estimated that the Sun", "Figure 2 shows the relation", "The optical spectrum of a galaxy",
       "A star has an effective temperature", "A star has visual apparent magnitude",
       "A binary system of stars consists", "Find the equatorial coordinates",
       "In the centre of our Galaxy", "What is the maximum altitude", "Sirius A, with visual magnitude",
       "Recently in London", "What is the hour angle", "The Doppler shift of three remote"]
# 2013: statements embedded in solutions
job("2013_th_sol.pdf",
    [P(f"2013_TH_S{i+1}", rf"^{i+1}\.\s*{re.escape(w[:16])}", stop_rx=r"^Answer") for i, w in enumerate(w13)] +
    [P("2013_TH_L1", r"^Question 1\b", stop_rx=r"^Answer"),
     P("2013_TH_L2", r"^Question 2\b", stop_rx=r"^Answer"),
     P("2013_TH_L3", r"^Question 3\b", stop_rx=r"^Answer")])
job("2013_th_sol.pdf",
    [P(f"2013_THSOL_S{i+1}", rf"^{i+1}\.\s*{re.escape(w[:16])}") for i, w in enumerate(w13)] +
    [P("2013_THSOL_L1", r"^Question 1\b"), P("2013_THSOL_L2", r"^Question 2\b"),
     P("2013_THSOL_L3", r"^Question 3\b")])

job("2013_da_sol.pdf",
    [P(f"2013_DA_D{i}", rf"^Question {i}\.", stop_rx=r"^Answer") for i in (1, 2, 3, 4)])
job("2013_da_sol.pdf",
    [P(f"2013_DASOL_D{i}", rf"^Question {i}\.") for i in (1, 2, 3, 4)])

t14 = ["Lagrange Points", "Sun gravitational catastrophe", "Cosmic radiation",
       "Mass function of a visual binary", "The Astronaut saved", "life", "The effective temperature on the surface",
       "Gradient temperatures", "Pressure of light", "The density of the star",
       "ship orbiting the Sun", "The Vega star in the mirror", "Stars with Romanian names",
       "Apparent magnitude of the Moon", "Absolute magnitude of a cephe"]
job("2014_th.pdf",
    [P(f"2014_TH_P{i+1}", rf"^Problem {i+1}\.") for i in range(15)] +
    [P("2014_TH_L1", r"^16\.\s*Long problem 1"), P("2014_TH_L2", r"^17\.\s*Long problem 2"),
     P("2014_TH_L3", r"^18\.\s*Long problem 3")])

job("2014_da.pdf", [P("2014_DA_D1", r"^Problem 1\b.*Black Hole|^Problem 1$"),
                    P("2014_DA_D2", r"^Problem 2\b.*Thermodynamic|^Problem 2$"),
                    P("2014_DA_D3", r"^Problem 3\b.*(IOAA|Observer)|^Problem 3$")])

# 2015: bare "N." on its own line
job("2015_th.pdf",
    [P(f"2015_TH_S{i}", rf"^{i}\.$") for i in range(1, 16)] +
    [P("2015_TH_L1", r"^1\.$"), P("2015_TH_L2", r"^2\.$"), P("2015_TH_L3", r"^3\.$")])

job("2015_da.pdf", [P("2015_DA_D1", r"^Problem 1$|^Problem 1\b"),
                    P("2015_DA_D2", r"^Problem 2$|^Problem 2\b")])

job("2016_theory.pdf", [P(f"2016_TH_T{i}", rf"^\(T{i}\)") for i in range(1, 13)])
job("2016_data_analysis.pdf", [P(f"2016_DA_D{i}", rf"^\(D{i}\)") for i in (1, 2, 3)])

job("2017_Theory.pdf", [P(f"2017_TH_T{i}", rf"^\(T{i}\)") for i in range(1, 14)])
job("2017_DataAnalysis.pdf", [P(f"2017_DA_D{i}", rf"^\(D{i}\)") for i in (1, 2)])

job("2018_18_th.pdf", [P(f"2018_TH_T{i}", rf"^\(T{i}\)") for i in range(1, 12)])
job("2018_18_da.pdf", [P(f"2018_DA_D{i}", rf"^\(D{i}\)") for i in (1, 2)])

t19 = ["Famous astronomical events", "Deflection of radio photons", "The supermassive black hole",
       "Improving a common reflecting", "Cosmic Microwave Background Oven", "The height of the chimney",
       "Effect of sunspots", "Amplitude variation of RR Lyrae", "Distance of the Lagrangian point",
       "South", "Identification of light curves", "Distance to a Near-Earth Asteroid",
       "Distance to the Coma galaxy cluster", "Photographing a nanosatellite"]
job("2019_th.pdf", [P(f"2019_TH_{i+1}", rf"^{i+1}\.\s*{re.escape(t[:20])}") for i, t in enumerate(t19)])
job("2019_da.pdf", [P("2019_DA_1", r"^1\.\s*Photometry and spectroscopy"),
                    P("2019_DA_2", r"^2\.\s*Triply eclipsing")])

t20 = ["Astrophotography", "Flat Earth", "Mirror", "Light Curves", "HII region",
       "Occultation of a", "Radiant of a Meteor Shower", "Jupiter"]
job("2020_th_sol.pdf",
    [P(f"2020_TH_{i+1}", rf"^{i+1}\s+{re.escape(t[:12])}|^{re.escape(t[:12])}", stop_rx=r"^Solution") for i, t in enumerate(t20)])
job("2020_th_sol.pdf",
    [P(f"2020_THSOL_{i+1}", rf"^{i+1}\s+{re.escape(t[:12])}|^{re.escape(t[:12])}") for i, t in enumerate(t20)])
d20 = ["AGN", "Minor Planet", "Hypervelocity stars"]
job("2020_da_sol.pdf",
    [P(f"2020_DA_{i+1}", rf"^{i+1}\s+{re.escape(t)}|^{re.escape(t)}$", stop_rx=r"^Solution") for i, t in enumerate(d20)])
job("2020_da_sol.pdf",
    [P(f"2020_DASOL_{i+1}", rf"^{i+1}\s+{re.escape(t)}|^{re.escape(t)}$") for i, t in enumerate(d20)])

# 2021: per-problem files; English statement only
for i in range(1, 16):
    job(f"2021_Q{i}.pdf", [P(f"2021_TH_Q{i}", r"English \(Official\)", stop_rx=r"Bulgarian \(Bulgaria\)")])
job("2021_Q1_da.pdf", [P("2021_DA_DA1", r"English \(Official\)", stop_rx=r"Bulgarian \(Bulgaria\)")])
job("2021_Q2_da.pdf", [P("2021_DA_DA2", r"English \(Official\)", stop_rx=r"Bulgarian \(Bulgaria\)")])

t22 = ["Planck", "Circumbinary planet", "Expanding ring nebula", "Journey Between Galaxies",
       "Flaring protoplanetary disk", "Photometry of Binary stars", "Georgia to Georgia",
       "Ring of a planet", "Solar Retrograde Motion", "Accretion", "Dyson Sphere",
       "Co-orbital satellites", "Relativistic Beaming"]
job("2022_Problems.pdf",
    [P(f"2022_TH_{i+1}", rf"^{re.escape(t)}.*\([0-9]+ [Pp]oints\)") for i, t in enumerate(t22)])
job("2022_da.pdf", [P("2022_DA_1", r"Gravitational wave astronomy.*\(45 points\)|^1\s+Gravitational wave"),
                    P("2022_DA_2", r"Galactic Surveys.*\(105 points\)|^2\s+Galactic Surveys")])

t23 = ["Neptune", "Magnetic Field", "Microlensing", "Europa", "Dark Energy", "Bolometer",
       "Libration", "Neutrinos", "Second eclipse", "Aldebaran",
       "X-ray emission from galaxy clusters", "DART", "LISA"]
job("2023_theory.pdf",
    [P(f"2023_TH_Q{i+1}", rf"^{re.escape(t)}\s*\([0-9]+ points\)") for i, t in enumerate(t23)])
job("2023_DA.pdf", [P("2023_DA_Q1", r"^Distance to the Large Magellanic Cloud\s*\(50 points\)"),
                    P("2023_DA_Q2", r"^Isolated black hole\s*\(75 points\)")])

t24 = ["Sundial", "Galaxy Cluster", "Asteroid", "White Dwarf", "CMB", "Cluster Photography",
       "Castaway", "Binary Hardening", "Physics of Accretion", "Greatest Eclipse", "Ground Tracks"]
job("2024_th.pdf", [P(f"2024_TH_T{i+1}", rf"^T{i+1}\.\s*{re.escape(t)}") for i, t in enumerate(t24)])
job("2024_da.pdf", [P("2024_DA_D1", r"^D1\.\s*Photometric comparison"),
                    P("2024_DA_D2", r"^D2\.\s*Shapley Hypothesis")])

job("2025_theory_questions.pdf", [P(f"2025_TH_T{i:02d}", rf"^\(T{i:02d}\)") for i in range(1, 13)])
job("2025_data_analysis_questions.pdf", [P(f"2025_DA_D{i:02d}", rf"^\(D{i:02d}\)") for i in (1, 2)])

# ---------------- SOLUTION PAPERS ----------------

job("2007_th_sol.pdf",
    [P(f"2007_THSOL_1.{i}", rf"^1\.{i}\b") for i in range(1, 16)] +
    [P("2007_THSOL_Q2", r"^QUESTION 2\b|A PLANET"), P("2007_THSOL_Q3", r"^QUESTION 3\b|BINARY SYSTEM"),
     P("2007_THSOL_Q4", r"^QUESTION 4\b|GRAVITATIONAL LENSING")])
job("2007_da_sol.pdf", [P(f"2007_DASOL_D{i}", rf"^Question {i}\b") for i in (1, 2, 3)])

job("2008_th_sol.pdf",
    [P(f"2008_THSOL_S{i+1}", rf"^{i+1}\.\s*{re.escape(w8[i][:18])}") for i in range(9)] +
    [P("2008_THSOL_L1", r"^10\.\s*An eclipsing binary")] +
    [P(f"2008_THSOL_S{i+1}", rf"^{i+1}\.\s*{re.escape(w8[i][:18])}") for i in range(10, 15)] +
    [P("2008_THSOL_S10", r"^1\.\s*The coordinates of the components"),
     P("2008_THSOL_L2", r"^2\.?\s*A UBV photometric"),
     P("2008_THSOL_L3", r"^3\.?\s*Measurement of the cosmic microwave")])
job("2008_da_sol.pdf", [P("2008_DASOL_D1", r"^I\.\s*Virgo Cluster"),
                        P("2008_DASOL_D2", r"^II\.\s*Determination|^II\."),
                        P("2008_DASOL_D3", r"^III\.\s*The Age|^III\.")])

# 2009/2010/2011/2012 scanned sols: page ranges from visual mapping (0-based)
def pages_job(file, prefix, ranges):
    job(file, [P(f"{prefix}{k}", pages=[a, b]) for k, (a, b) in ranges.items()])

pages_job("2009_th_sol.pdf", "2009_THSOL_P", {
    1:(0,0), 2:(0,1), 3:(1,2), 4:(2,3), 5:(3,4), 6:(4,6), 7:(6,6), 8:(7,7), 9:(7,8),
    10:(8,9), 11:(9,9), 12:(9,10), 13:(11,11), 14:(12,12), 15:(12,14), 16:(13,17), 17:(17,21)})
pages_job("2009_da_sol.pdf", "2009_DASOL_D", {1:(0,3), 2:(4,9)})
pages_job("2010_da_sol.pdf", "2010_DASOL_D", {1:(0,2), 2:(3,4)})
job("2011_th_sol.pdf",
    [P(f"2011_THSOL_S{k}", pages=list(v)) for k, v in
     {1:(0,0),2:(0,0),3:(0,0),4:(1,1),5:(2,2),6:(2,2),7:(2,2),8:(3,3),9:(3,3),10:(4,4),
      11:(4,4),12:(4,4),13:(4,5),14:(5,5),15:(5,5)}.items()] +
    [P("2011_THSOL_L1", pages=[6,6]), P("2011_THSOL_L2", pages=[7,8]), P("2011_THSOL_L3", pages=[9,9])])
pages_job("2011_da_sol.pdf", "2011_DASOL_D", {1:(0,2), 2:(3,4)})
job("2012_th_sol.pdf",
    [P(f"2012_THSOL_S{k}", pages=list(v)) for k, v in
     {1:(0,0),2:(0,0),3:(1,1),4:(1,1),5:(1,1),6:(1,1),7:(1,2),8:(2,2),9:(2,3),10:(3,4),
      11:(4,4),12:(4,5),13:(5,5),14:(5,6),15:(6,7)}.items()] +
    [P("2012_THSOL_L1", pages=[7,8]), P("2012_THSOL_L2", pages=[8,10])])
job("2012_da_sol.pdf", [P("2012_DASOL_D1", r"^Question 1\b"), P("2012_DASOL_D2", r"^Question 2\b")])

job("2014_th_sol.pdf",
    [P(f"2014_THSOL_P{i+1}", rf"^Problem {i+1}\.") for i in range(15)] +
    [P("2014_THSOL_L1", r"Long problem 1|LONG PROBLEM 1"), P("2014_THSOL_L2", r"Long problem 2|LONG PROBLEM 2"),
     P("2014_THSOL_L3", r"Long problem 3|LONG PROBLEM 3")], start_page=1)
job("2014_da_sol.pdf", [P("2014_DASOL_D1", r"^Problem 2\b.*Black Hole"),
                        P("2014_DASOL_D2", r"^Problem 3\b|Extra solar tests"),
                        P("2014_DASOL_D3", r"^B\.\s*Observer on an extrasolar")], start_page=1)

job("2015_th_sol.pdf",
    [P(f"2015_THSOL_S{i}", rf"^{i}\.$") for i in range(1, 16)] +
    [P("2015_THSOL_L1", r"^LONG QUESTIONS"), P("2015_THSOL_L2", r"^2\.\s*Two massive stars"),
     P("2015_THSOL_L3", r"^3\.\s*Suppose a static spherical")])
job("2015_da_sol.pdf", [P("2015_DASOL_D1", r"^Solution of Problem 1"),
                        P("2015_DASOL_D2", r"^Solution of Problem 2")])

job("2016_theory_sol.pdf", [P(f"2016_THSOL_T{i}", rf"^\(T{i}\)") for i in range(1, 13)])
job("2016_data_analysis_sol.pdf", [P(f"2016_DASOL_D{i}", rf"^\(D{i}\)") for i in (1, 2, 3)])
job("2017_Theory_Solution.pdf",
    [P(f"2017_THSOL_T{i}", (rf"^\(T{i}\)" if i != 9 else r"^\(T9\)|^Galactic Outflow$")) for i in range(1, 14)])
job("2017_DataAnalysis_Solution.pdf", [P(f"2017_DASOL_D{i}", rf"^\(D{i}\)") for i in (1, 2)])
job("2018_18_th_sol.pdf", [P(f"2018_THSOL_T{i}", rf"^\(T{i}\)") for i in range(1, 12)])
job("2018_18_da_sol.pdf", [P(f"2018_DASOL_D{i}", rf"^\(D{i}\)") for i in (1, 2)])
t19s = {2: r"^2\.\s*De", 7: r"^7\.\s*E", 11: r"^11\.\s*Ident"}
job("2019_th_sol.pdf", [P(f"2019_THSOL_{i+1}", t19s.get(i+1, rf"^{i+1}\.\s*{re.escape(t[:20])}")) for i, t in enumerate(t19)])
job("2019_da_sol.pdf", [P("2019_DASOL_1", r"^1\.\s*Photometry and spectroscopy"),
                        P("2019_DASOL_2", r"^2\.\s*Triply eclipsing")])

for i in range(1, 16):
    job(f"2021_T{i}_Solution.pdf", [P(f"2021_THSOL_Q{i}", whole=True)])
job("2021_DA1_solution.pdf", [P("2021_DASOL_DA1", whole=True)])
job("2021_DA2_solution.pdf", [P("2021_DASOL_DA2", whole=True)])

s22 = list(t22); s22[7] = "Saturn"
job("2022_Solutions.pdf",
    [P(f"2022_THSOL_{i+1}", rf"^Solution:\s*{re.escape(t)}") for i, t in enumerate(s22)])
job("2022_da_1_sol.pdf", [P("2022_DASOL_1", whole=True)])
job("2022_da_2_sol.pdf", [P("2022_DASOL_2", whole=True)])

pg23 = {6:(10,11), 7:(12,13), 8:(14,15), 9:(16,21), 10:(22,25)}
job("2023_th_solutions.pdf",
    [P(f"2023_THSOL_Q{i+1}", rf"^Theory {i+1}:") if (i+1) not in pg23
     else P(f"2023_THSOL_Q{i+1}", pages=list(pg23[i+1])) for i in range(13)])
job("2023_DA_sol.pdf", [P("2023_DASOL_Q1", r"Distance to the Large Magellanic Cloud"),
                        P("2023_DASOL_Q2", r"Isolated black hole")])

job("2024_th_sol.pdf", [P(f"2024_THSOL_T{i+1}", rf"^T{i+1}\.\s*{re.escape(t)}") for i, t in enumerate(t24)])
job("2024_da_sol.pdf", [P("2024_DASOL_D1", r"^D1\.\s*Photometric comparison"),
                        P("2024_DASOL_D2", r"^D2\.\s*Shapley Hypothesis")])
job("2025_theory_solution.pdf", [P(f"2025_THSOL_T{i:02d}", rf"^\(T{i:02d}\)") for i in range(1, 13)])
job("2025_data_analysis_solutions.pdf", [P(f"2025_DASOL_D{i:02d}", rf"^\(D{i:02d}\)") for i in (1, 2)])

json.dump(J, open("config_all.json", "w"), indent=1)
print(f"{len(J)} jobs, {sum(len(j['problems']) for j in J)} snippets")
