from brian2 import *

# # Simple model 1
# start_scope()
#
# tau = 10*ms
# eqs = ''' dv/dt = (1-v)/tau : 1 ''' # differential equotation
# G = NeuronGroup(1, eqs, method = 'exact') # Creating neuron
# M = StateMonitor(G, 'v', record=True)
# print('Before v = %s' % G.v[0])
# run(100*ms)
# print('After v = %s' % G.v[0])
# print('Expected value of v = %s' % (1-exp(-100*ms/tau)))
# plot(M.t/ms, M.v[0], 'C0', label='Brian')
# plot(M.t/ms, 1-exp(-M.t/tau), 'C1--',label='Analytic')
# xlabel('Time (ms)')
# ylabel('v')
# legend()
# show()


## Simple model 2
# start_scope()
#
# tau = 10*ms
# eqs = '''dv/dt = (sin(2*pi+100*Hz*t)-v)/tau : 1'''
# G = NeuronGroup(1, eqs, method = 'euler')
# M = StateMonitor(G, 'v', record = 0)
# G.v = 5
# run(60*ms)
# plot(M.t/ms, M.v[0])
# xlabel('Time (ms)')
# ylabel('v')
# show()
#
# # Adding spikes, refractory - 1 neuron
# start_scope()
#
# tau = 5*ms
# eqs = '''dv/dt = (1-v)/tau : 1 (unless refractory)'''
# G = NeuronGroup(1, eqs, threshold= 'v>0.8', reset = 'v = 0', refractory=5*ms ,method = 'exact')
# statemon = StateMonitor(G, 'v', record = 0)
# spikemon = SpikeMonitor(G)
#
# run(70*ms)
# for t in spikemon.t:
#     axvline(t/ms, ls = '--', c = 'C1', lw = 3)
# plot(statemon.t/ms, statemon.v[0])
#
#
# xlabel('Time (ms)')
# ylabel('v')
# print('Spike times: %s' % spikemon.t[:])
#
# show()

## Multiple neurons
start_scope()

N = 100 # Number of neurons
tau = 10 * ms
eqs = '''dv/dt = (2-v)/tau : 1 (unless refractory)'''
G = NeuronGroup(N, eqs, threshold = 'v > 0.8', reset = 'v = 0', method = 'exact', refractory= 5* ms)
G.v = 'rand()'

spikemon = SpikeMonitor(G)
statemon = StateMonitor(G, 'v',record = [0, 10])


run(70 * ms)

subplot(2,1,1)
plot(statemon.t/ms, statemon.v[1]/mV, label='v')
axhline(800, ls = '--', c = 'C1', lw = 1)
spikes_10 = [i for  i,e in enumerate(spikemon.i) if e == 10]
for index in spikes_10:
    axvline(spikemon.t[index]/ms, ls = '--', c = 'C1', lw = 2)

xlabel('Time (ms)')
ylabel('v')
title('Value for Neuron 10')

subplot(2,1,2)
plot(spikemon.t/ms, spikemon.i,  '.k')
for index in spikes_10:
    plot(spikemon.t[index]/ms, spikemon.i[index],  '.k', c = 'C2', lw = 5)
    axvline(spikemon.t[index] / ms, ls='--', c='C1', lw=1)
plot(70,0)
axhline(10, ls = '--', c = 'C1', lw = 1)

xlabel('Time (ms)')
ylabel('Neuron index')

rate = spikemon.count[99]/(70 *ms)
print(f"firing rate is {rate:.2f} Hz")

show()

## Parameters
# start_scope()
#
# N = 100
# tau = 10 * ms
# v0_max = 3.0
# duration = 1000 * ms
#
# eqs = '''
# dv/dt = (v0-v)/tau : 1 (unless refractory)
# v0 : 1
# '''
# ## v0 :1 - dimensionless
#
# G = NeuronGroup(N, eqs, threshold = 'v > 1', reset = 'v = 0', refractory = '5*ms', method = 'exact')
# spikemon = SpikeMonitor(G)
#
#
# ## Initialises the value of v0 for each neuron varying from 0 up to v0_max.
# # The symbol i when it appears in strings like this refers to the neuron index.
# G.v0 = 'i * v0_max/(N-1)'
#
# run(duration)
#
# figure(figsize = (12,4))
# subplot(121)
# plot(spikemon.t/ms,spikemon.i, '.k')
# xlabel('Time (ms)')
# ylabel('Neuron index')
# subplot(122)
# plot(G.v0, spikemon.count/duration)
# xlabel('v0')
# ylabel('Firing rate (sp/s)')
#
# show()

## Stochastic neurons
# start_scope()
#
# N = 100
# tau = 10*ms
# v0_max = 3.
# duration = 1000*ms
# sigma = 0.2
#
# eqs = '''
# dv/dt = (v0-v)/tau+sigma*xi*tau**-0.5 : 1 (unless refractory)
# v0 : 1
# '''
#
# G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0', refractory=5*ms, method='euler')
# M = SpikeMonitor(G)
#
# G.v0 = 'i*v0_max/(N-1)'
#
# run(duration)
#
# figure()
# subplot(121)
# plot(M.t/ms, M.i, '.k')
# xlabel('Time (ms)')
# ylabel('Neuron index')
# subplot(122)
# plot(G.v0, M.count/duration)
# xlabel('v0')
# ylabel('Firing rate (sp/s)')
#
# show()

## End of Tutorial (Nic nie robi bo nie działa xD)

# start_scope()
#
# N = 1000
# tau = 10*ms
# vr = -70*mV
# vt0 = -50*mV
# delta_vt0 = 5*mV
# tau_t = 100*ms
# sigma = 0.5*(vt0-vr)
# v_drive = 2*(vt0-vr)
# duration = 100*ms
#
# eqs = '''
# dv/dt = (v_drive+vr-v)/tau + sigma*xi*tau**-0.5 : volt
# dvt/dt = (vt0-vt)/tau_t : volt
# '''
#
# reset = '''
# v = vr
# vt += delta_vt0
# '''
#
# G = NeuronGroup(N, eqs, threshold='v>vt', reset=reset, refractory=5*ms, method='euler')
# spikemon = SpikeMonitor(G)
#
# G.v = 'rand()*(vt0-vr)+vr'
# G.vt = vt0
#
# run(duration)
#
# _ = hist(spikemon.t/ms, 100, histtype='stepfilled', facecolor='k', weights=list(ones(len(spikemon))/(N*defaultclock.dt)))
# xlabel('Time (ms)')
# ylabel('Instantaneous firing rate (sp/s)');
#
# show()



