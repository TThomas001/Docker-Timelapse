"""
author: @thomas-chen
date: 2023-01-01
description:This is the script that combines all snapshot photos into a video. The images will be deleted after the video is created.
"""
import os
import shutil

import cv2
import argparse
import glob

import logging
import logging.config
import logging.handlers

def main():
    print("yes! I am runing just fine")
    parser = argparse.ArgumentParser(description="This is the script that combines all snapshot photos into a video")
    parser.add_argument("-i", "--input", help="The input directory that contains all the snapshot photos",
                        required=True)
    parser.add_argument("-o", "--output", help="The output video file")
    parser.add_argument("-f", "--fps", help="The FPS of the output video", required=True)
    parser.add_argument("-d", "--debug", help="Enable debug mode", action="store_true")
    args = parser.parse_args()
    
    # set up logging
    log_file = os.path.join(args.input, "video.log")
    # check if log file exists
    if not os.path.exists(log_file):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(filename=log_file, level=logging.DEBUG if args.debug else logging.INFO,format='%(asctime)s %('
                                                                                                      'levelname)s %('
                                                                                                      'message)s',datefmt='%H:%M:%S')

    logger = logging.getLogger("time_lapse")
    # get image folder with date format YYYY-MM-DD
    image_folder = sorted(glob.glob(os.path.join(args.input, "20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]")),key=os.path.getmtime)
    # sort the folder by date
    # get image file names
    # get all the snapshot photos
    logger.info("Getting all the snapshot photos")
    photo_list = glob.glob(os.path.join(image_folder[0], "*.jpg"))
    photo_list.sort()
    logger.info("Found {} snapshot photos".format(len(photo_list)))
    logger.debug("Snapshot photos: {}".format(photo_list))

    # get the size of the first snapshot photo
    logger.info("Getting the size of the first snapshot photo")
    img = cv2.imread(photo_list[0])
    height, width, layers = img.shape
    size = (width, height)
    logger.info("Size of the first snapshot photo: {}".format(size))

    # create the video writer
    logger.info("Creating the video writer")
    output_video = args.output if args.output else image_folder[0] + ".mp4"
    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*"mp4v"),
                          int(args.fps), size)

    # write each snapshot photo to the video writer
    logger.info("Writing each snapshot photo to the video writer")
    for photo in photo_list:
        img = cv2.imread(photo)
        out.write(img)

    # release the video writer
    logger.info("Releasing the video writer")
    out.release()

    # clean up
    shutil.rmtree(image_folder[0])
    logger.info("Deleted the input directory")
    logger.info("Cleaning up")
    logger.info("Done")

if __name__ == "__main__":
    main()


