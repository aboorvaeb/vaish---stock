import monte_carlo as mc

sim = mc.monte_carlo('AAPL')

sim.plot_historical_data()

sim.brownian_motion(200,1000)
