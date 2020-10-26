# Usage

First build the docker image. In the root of the repo run
```
dts devel build -f
```

Record the name of the built image.

To run the image
```
docker run --rm -v <directory containing bag>:/bags -e BAG_NAME="name of the bag file" <name of image built in the previous step>
```

For example

```
docker run --rm -v ~/bags/:/bags -e BAG_NAME="cam_april.bag" duckietown/processing-bags-rh3:v2-amd64
```
Would process the bag file `cam_april.bag` containing image message in the directory `~/bags` using the built image called `duckietown/analyze-bags-rh3:v2-amd64`. It will write a bag file with the processed images to a file called `cam_april_processed.bag` in the same directory mounted on the container