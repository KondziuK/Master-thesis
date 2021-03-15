from brian2 import *

# # Parameters
# num_inputs = 100
# input_rate =10 * Hz
# weight = 0.1
# tau_range = linspace(1, 10, 30) * ms
# num_tau = len(tau_range)
#
# eqs = '''
# dv/dt = -v/tau :1
# tau : second
# '''
# P = PoissonGroup(num_inputs, rates=input_rate)
#
# G = NeuronGroup(num_tau, eqs, threshold='v>1', reset='v=0', method='exact')
# G.tau = tau_range
#
# S = Synapses(P, G, on_pre='v += weight')
# S.connect()
# M = SpikeMonitor(G)
#
# run(1 * second)
# run(1*second)
# output_rates = M.count/second # firing rate is count/duration
# plot(tau_range/ms, output_rates)
# xlabel(r'$\tau$ (ms)')
# ylabel('Firing rate (sp/s)');
#
# figure()
# trains = M.spike_trains()
# isi_mu = full(num_tau, nan)*second
# isi_std = full(num_tau, nan)*second
# for idx in range(num_tau):
#     train = diff(trains[idx])
#     if len(train)>1:
#         isi_mu[idx] = mean(train)
#         isi_std[idx] = std(train)
# errorbar(tau_range/ms, isi_mu/ms, yerr=isi_std/ms)
# xlabel(r'$\tau$ (ms)')
# ylabel('Interspike interval (ms)')
#
# show()


### Adding input

# start_scope()
#
# A = 2.5
# f = 10 * Hz
# tau = 5 * ms
# # Create a TimedArray and set the equatations to use it
# t_recorded = arange(int(200*ms/defaultclock.dt))*defaultclock.dt
# I_recorded = TimedArray(A*sin(2*pi*f*t_recorded), dt=defaultclock.dt)
# eqs = '''
# dv/dt = (I-v)/tau : 1
# I = I_recorded(t) : 1
# '''
# G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
# M =StateMonitor(G, variables=True, record=True)
# run(200*ms)
# plot(M.t/ms, M.v[0], label = 'v')
# plot(M.t/ms, M.I[0], label='I')
# xlabel('Time (ms)')
# ylabel('v')
# legend(loc='best')
# show()


#
# start_scope()
# A = 2.5
# f = 10*Hz
# tau = 5*ms
# # Let's create an array that couldn't be
# # reproduced with a formula
# num_samples = int(200*ms/defaultclock.dt)
# I_arr = zeros(num_samples)
# for _ in range(100):
#     a = randint(num_samples)
#     I_arr[a:a+100] = rand()
# I_recorded = TimedArray(A*I_arr, dt=defaultclock.dt)
# eqs = '''
# dv/dt = (I-v)/tau : 1
# I = I_recorded(t) : 1
# '''
# G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
# M = StateMonitor(G, variables=True, record=True)
# run(200*ms)
# plot(M.t/ms, M.v[0], label='v')
# plot(M.t/ms, M.I[0], label='I')
# xlabel('Time (ms)')
# ylabel('v')
# legend(loc='best');
# show()


### Last one

start_scope()
from matplotlib.image import imread
img = (1-imread('brian.png'))[::-1, :, 0].T
num_samples, N = img.shape
ta = TimedArray(img, dt=1*ms) # 228
A = 1.5
tau = 2*ms
eqs = '''
dv/dt = (A*ta(t, i)-v)/tau+0.8*xi*tau**-0.5 : 1
'''
G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0', method='euler')
M = SpikeMonitor(G)
run(num_samples*ms)
plot(M.t/ms, M.i, '.k', ms=3)
xlim(0, num_samples)
ylim(0, N)
xlabel('Time (ms)')
ylabel('Neuron index');
show()