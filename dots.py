import glob
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

#number of random dots to make up the sphere
NUM_DOTS = 2500

# for video conversion (higher frames per second = smoother video)
FRAMES = 200
FRAME_RATE = '16'
OUTPUT_FILE = 'dots.mp4'


# furthest a dot can move horizontally in a frame
MAX_X_MOVEMENT = 0.02
# home much faster  dots should travel when moving eastward
EAST_TO_WEST_RATIO = .75

# furthest a dot can move vertically in a frame
MAX_Y_MOVEMENT = 0.001

# create random dots
# range is 0 to 2 so that we can use a modulo to keep them inside the window
# we'll shift them to -1, 1 later
xs = np.random.uniform(0, 2, (NUM_DOTS,1))
ys = np.random.uniform(0, 2, (NUM_DOTS,1))

# consistently choose some dots to move westward & others to move eastward
# apply the ratio so that eastward dots move slower than westward dots
choices = np.random.choice([-MAX_X_MOVEMENT,EAST_TO_WEST_RATIO * MAX_X_MOVEMENT], size=(NUM_DOTS,1))


for i in tqdm(range(FRAMES)):
    # we want dots to move faster as they approach the center of the sphere
    # so we'll apply a sine function to the y values with an pi/2 expansion to account for the (0,2) range
    xs +=  choices * np.abs(np.sin(0.5 * np.pi * ys))
    # keep dots inside the window
    xs = np.mod(xs, 2)

    # add a tiny bit of random vertical noise
    ys += np.random.uniform(0.0, MAX_Y_MOVEMENT, (NUM_DOTS,1))
    ys = np.mod(ys, 2)

    # shift the range from (0,2) to (-1,1)
    # and clip dots to a circle of radius 1
    plotxs = xs - 1
    plotys = ys - 1
    mask = np.sqrt(plotxs**2 + plotys**2) < 1
    plt.scatter(plotxs[mask], plotys[mask], s=3)

    # save the frame
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('dots_{:02d}.png'.format(i), dpi=300)
    plt.clf()

# convert the frames to a video
subprocess.call([
        'ffmpeg', '-framerate', FRAME_RATE, '-i', 'dots_%02d.png', '-r', '30', '-pix_fmt', 'yuv420p',
        OUTPUT_FILE
    ])

for file_name in tqdm(glob.glob("*.png")):
    os.remove(file_name)