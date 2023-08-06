"""
Perform inference on a trained model using TensorFlow.

Author: Ivan Lobato
Email: Ivanlh20@gmail.com
"""
import os
import numpy as np
import matplotlib

# Check if running on remote SSH and use appropriate backend for matplotlib
remote_ssh = "SSH_CONNECTION" in os.environ
matplotlib.use('Agg' if remote_ssh else 'TkAgg')
import matplotlib.pyplot as plt

from rc_cbed.model import load_rc_cbed_net, load_test_data

def fcn_inference():
    x, y = load_test_data()

    net_r_cbed = load_rc_cbed_net()
    net_r_cbed.summary()

    n_data = x.shape[0]
    batch_size = 16
    
    n = [1.0, 0.50, 0.25]

    y_p = net_r_cbed.predict(x, batch_size)

    fig = plt.figure(figsize=(12, 6))

    for ik in range(n_data):
        x_ik = x[ik, :, :, 0].squeeze()
        y_t_ik = y[ik, :, :, 0].squeeze()
        y_p_ik = y_p[ik, :, :, 0].squeeze()

        for it in range(3):
            ax = plt.subplot(3, 3, it*3+1)
            ax.imshow(np.power(x_ik, n[it]), interpolation='none', cmap='viridis')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(False)
            ax.set_title("Det. CBED^{:3.2f}".format(n[it]), fontsize=14)
            # plt.colorbar(ax)

            ax = plt.subplot(3, 3, it*3+2)
            ax.imshow(np.power(y_p_ik, n[it]), interpolation='none', cmap='viridis')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(False)
            ax.set_title("Rest-Ctr. CBED^{:3.2f}".format(n[it]), fontsize=14)
            # plt.colorbar(ax)

            ax = plt.subplot(3, 3, it*3+3)
            ax.imshow(np.power(y_t_ik, n[it]), interpolation='none', cmap='viridis')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(False)
            ax.set_title("GT CBED^{:3.2f}".format(n[it]), fontsize=14)
            # plt.colorbar(ax)

        if remote_ssh:
            plt.savefig("rc_cbed.png", format='png')
        else:
            fig.show()

        print(ik)

if __name__ == '__main__':
    fcn_inference()