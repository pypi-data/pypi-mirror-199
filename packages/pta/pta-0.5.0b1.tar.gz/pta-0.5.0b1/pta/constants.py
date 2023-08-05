"""Constants used in tha PTA package.
"""

from enkie.distributions import LogNormalDistribution

default_min_eigenvalue_tds_basis = 1e-3
"""Default minimum eigenvalue for vector of the basis of the thermodynamic space."""
default_log_conc = LogNormalDistribution(-8.3371, 1.9885)
"""Default distribution of metabolite concentrations."""
default_flux_bound = 1000
"""Default magnitude of lower/upper bounds of fluxes."""

# PMO and TFS
default_confidence_level = 0.95
"""Default confidence level for PMO problems and TFS"""
default_min_drg = 0.1
"""Default minimum DrG magnitude for PMO problems and TFS"""
default_max_drg = 1000
"""Default maximum DrG magnitude for PMO problems and TFS"""

# Thermodynamic assessment.
non_intracellular_compartment_ids = ["e", "p"]
"""Identifiers of non-intracellular compartments."""
default_theta_z = 1.0
"""Default threshold on the z-score to consider a predicted value an anomaly."""
default_theta_s = 0.1
"""Default threshold on the shadow price to consider a reaction a strong thermodynamic
constrain."""
default_max_non_intracellular_conc_mM = 10
"""Default threshold on the concentration to consider a predicted concentration an
anomaly."""

# Sampling.
default_min_chains = 4
"""Minimum number of chains to use  by default.
"""
default_num_samples = 1000
"""Default number of samples to store.
"""
us_steps_multiplier = 64
"""Coefficient for the number of steps sampling a flux space.
"""
tfs_steps_multiplier = 100
"""Coefficient for the number of steps sampling a thermodynamic space.
"""
tfs_default_feasibility_cache_size = 10000
"""Size of the cache storing whether encountered orthants are feasible or not.
"""
tfs_default_min_rel_region_length = 1e-6
"""Minimum relative size for an orthant to be considered during Hit-and-Run.
"""
default_max_psrf = 1.1
"""Default treshold on the Potential Scale Reduction Factors (PSRFs).
"""
default_max_threads = 2**10

min_samples_per_chain = 100
"""Minimum number of samples that must be drawn from each chain in order to obtain a
meaningful PSRF score."""
