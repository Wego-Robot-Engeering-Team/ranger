# Data Manual

## 개요
이 프로젝트의 데이터 bringup 기준 런치는 `wego/launch/teleop_launch.py` 입니다.

이 런치는 아래 노드들을 실행합니다.
- `ranger_base_node`
- `vectornav`
- `vn_sensor_msgs`
- `laser_scan_merger`
- `ekf_filter_node_odom`
- 선택 사항: `rviz2`

## 실행 방법
워크스페이스 루트에서 실행합니다.

```bash
ros2 launch wego teleop_launch.py
```

RViz까지 함께 실행하려면:

```bash
ros2 launch wego teleop_launch.py gui:=true
```

## 주요 런치 파일
- Base: `ranger_ros2/ranger_base/launch/ranger.launch.py`
- IMU: `wego_sensors/vectornav/vectornav/launch/vectornav.launch.py`
- Scan merger: `scan_merger_2/launch/dual_s3_scan_merger.launch.py`
- EKF: `robot_localization/launch/ranger_ekf.launch.py`

## 주요 토픽
- 전면 라이다: `/frontS3/scan`
- 후면 라이다: `/rearS3/scan`
- 머지된 스캔: `/scan_filtered`
- 머지된 포인트클라우드: `/merged/points`
- 원본 오도메트리: `/odom`
- EKF 오도메트리: `/odometry/local`
- IMU: `/vectornav/imu`

## 센서 장착 위치
현재 프로젝트 기본값은 `base_link` 기준 아래 위치를 가정합니다.

### 전면 S3 라이다
- `x`: `0.61 m`
- `y`: `0.0 m`
- `z`: `0.28 m`
- `roll`: `0.0`
- `pitch`: `0.0`
- `yaw`: `pi`

### 후면 S3 라이다
- `x`: `-0.61 m`
- `y`: `0.0 m`
- `z`: `0.28 m`
- `roll`: `0.0`
- `pitch`: `0.0`
- `yaw`: `0.0`

### VectorNav IMU
- `x`: `0.0 m`
- `y`: `0.0 m`
- `z`: `0.28 m`
- `roll`: `0.0`
- `pitch`: `0.0`
- `yaw`: `0.0`

## 현재 Scan Merger 기본값
- `target_frame_id`: `base_link`
- `fixed_frame_id`: `base_link`
- `ranges_num`: `1440`
- `min_scanner_range`: `0.05`
- `max_scanner_range`: `30.0`
- `min_x_range`: `-30.0`
- `max_x_range`: `30.0`
- `min_y_range`: `-30.0`
- `max_y_range`: `30.0`

## 로봇 바디 필터
`base_link` 기준 아래 직사각형 안에 들어오는 점들은 제거됩니다.
- `x`: `-0.60 ~ 0.60 m`
- `y`: `-0.45 ~ 0.45 m`

## 참고 사항
- `/scan_filtered`의 빈 빔은 `NaN`이 아니라 `+Inf`로 발행됩니다.
- `teleop_launch.py`는 현재 `body_min_x`, `body_max_x`만 override로 넘깁니다. `body_min_y`, `body_max_y`도 실행 시 바꾸고 싶으면 `wego/launch/teleop_launch.py`에 인자를 추가해야 합니다.
- `ranger_base_node`는 `publish_odom_tf:=false`로 실행되므로 TF 체인은 EKF 또는 localization 설정에 의존합니다.
- 전면 S3와 후면 S3 라이다는 절대 바꾸면 안 됩니다. `/frontS3/scan`은 `front_s3_laser`, `/rearS3/scan`은 `rear_s3_laser`와 그대로 매칭되어야 합니다.
- 전후면 라이다의 케이블, 디바이스 이름, frame id가 뒤바뀌면 둘 다 정상 발행 중이어도 `/scan_filtered` 형상이 틀어집니다.

## 빠른 확인 명령
```bash
ros2 topic echo /scan_filtered --once
ros2 topic echo /odometry/local --once
ros2 node list
```
