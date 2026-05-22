Every time the Brogue source code is updated, GitHub automatically builds the latest changes and puts them up for download.
This means that if you want to test the latest in-development version, you can do so without having to build the game yourself.

### Instructions

1. Go to the [GitHub Actions page for Brogue CE](https://github.com/tmewett/BrogueCE/actions).

1. Pick a branch.
'release' is for the next patch-level release (e.g. 1.8.1 -> 1.8.2), and 'master' is for the next minor-point release (e.g. 1.8.1 -> 1.9).

1. Click the latest run for that branch to go to the run overview page.
Scroll down to _Artifacts_ and download the one for your platform.

1. Extract the artifact (and the release archive inside it) and play!

### What's new?

We don't automatically generate change-logs for dev builds yet, but you can see all changes by looking at the files in the `changes/` folder in the code.