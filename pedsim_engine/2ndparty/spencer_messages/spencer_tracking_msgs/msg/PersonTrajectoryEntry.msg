# Message defining an entry of a person trajectory.
#

time     stamp           # age of the track
bool     is_occluded     # if the track is currently not matched by a detection
string   detection_id    # id of the corresponding detection in the current cycle (undefined if occluded)

# The following fields are extracted from the Kalman state x and its covariance C

geometry_msgs/PoseWithCovariance    pose   # pose of the track (z value and orientation might not be set, check if corresponding variance on diagonal is > 99999)
geometry_msgs/TwistWithCovariance   twist  # velocity of the track (z value and rotational velocities might not be set, check if corresponding variance on diagonal is > 99999)
