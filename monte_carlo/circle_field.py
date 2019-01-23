import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def generate_pts(N):
    '''
    Generates N uniformly distributed 2d points in square [-1, 1]
    and splits them into two subsets:
    pts_in -  points with norm < 1
    pts_out - points with norm > 1
    '''
    pts = np.array([np.random.uniform(-1, 1, N),
                    np.random.uniform(-1, 1, N)])
    dsts = np.linalg.norm(pts, axis=0)
    pts_in = pts[:, dsts <= 1]
    pts_out = pts[:, dsts > 1]
    return pts_in, pts_out


def monte_carlo_pi(no_of_points_in, no_of_all_points):
    '''
    Monte Carlo way of predicting PI value.
    It's number of points inside circle
    divided by number of all points
    and mulitplied by 4.
    '''
    return no_of_points_in / no_of_all_points * 4


if __name__ == '__main__':

    sns.set()
    mpis, npis, ims = [], [], []
    Ns = np.arange(100, 6000, 100)
    # initialize figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    for N in Ns:
        pts_in, pts_out = generate_pts(N)
        len_in = pts_in.shape[1]
        len_all = len_in + pts_out.shape[1]
        mpis.append(monte_carlo_pi(len_in, len_all))
        npis.append(N)
        im11 = ax1.scatter(pts_in[0, :],
                           pts_in[1, :],
                           marker='.',
                           color='red')
        im12 = ax1.scatter(pts_out[0, :],
                           pts_out[1, :],
                           marker='.',
                           color='blue')
        im13 = ax1.text(0.9, 1.0, N)
        im21 = ax2.scatter(npis[-1], mpis[-1],
                           marker='o', color='blue')
        ims.append([im11, im12, im13, im21])
    # Plot static line of PI aproximation progress
    # and actual value of PI
    ax2.plot(npis, mpis, marker='.', color='red')
    ax2.plot([Ns[0], Ns[-1]], [np.pi, np.pi],
             color='blue', linestyle='dashed')
    # Create Animation object
    ani = animation.ArtistAnimation(fig, ims, interval=100, blit=False,
                                    repeat_delay=10000)
    # and show it
    plt.show()



