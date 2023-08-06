try:
    import SimPEG.dask.simulation
    import SimPEG.dask.electromagnetics.static.resistivity.simulation
    import SimPEG.dask.electromagnetics.static.resistivity.simulation_2d
    import SimPEG.dask.electromagnetics.static.resistivity.receivers
    import SimPEG.dask.electromagnetics.static.induced_polarization.simulation
    import SimPEG.dask.electromagnetics.static.induced_polarization.simulation_2d
    import SimPEG.dask.electromagnetics.frequency_domain.simulation
    import SimPEG.dask.electromagnetics.time_domain.simulation
    import SimPEG.dask.potential_fields.base
    import SimPEG.dask.potential_fields.gravity.simulation
    import SimPEG.dask.potential_fields.magnetics.simulation
    import SimPEG.dask.objective_function
    import SimPEG.dask.data_misfit
    import SimPEG.dask.optimization
    import SimPEG.dask.inverse_problem

except ImportError as err:
    print("unable to load dask operations")
    print(err)
