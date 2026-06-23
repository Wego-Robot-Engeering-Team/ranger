# SLAM Manual

## 개요
SLAM bringup 기준 런치는 `wego/launch/slam_launch.py` 입니다.

이 런치는 아래 항목을 실행합니다.
- `slam_toolbox` online async 모드
- 선택 사항: `rviz2`

데이터 bringup은 `slam_launch.py`에 포함되어 있지 않습니다.
센서, 베이스, EKF는 먼저 별도로 실행해야 합니다.

## 실행 방법
워크스페이스 루트에서 아래 순서로 실행합니다.

```bash
ros2 launch wego teleop_launch.py
ros2 launch wego slam_launch.py
```

RViz 없이 SLAM만 띄우려면:

```bash
ros2 launch wego teleop_launch.py
ros2 launch wego slam_launch.py slam_gui:=false
```

## 주요 파일
- 런치: `wego/launch/slam_launch.py`
- SLAM 설정: `wego/config/slam_toolbox_2d.yaml`
- RViz 설정: `wego/rviz/slam.rviz`

## 현재 SLAM 기본값
- `odom_frame`: `odom`
- `map_frame`: `map`
- `base_frame`: `base_link`
- `scan_topic`: `/scan_filtered`
- `resolution`: `0.05`
- `min_laser_range`: `0.05`
- `max_laser_range`: `10.0`
- `mode`: `mapping`

## 기대하는 TF 체인
SLAM 중에는 아래 TF 체인이 형성되어야 합니다.

```text
map -> odom -> base_link
```

- `slam_toolbox`가 `map -> odom`을 발행합니다.
- Base / EKF가 `odom -> base_link`를 제공합니다.

## 주요 토픽
- 스캔 입력: `/scan_filtered`
- 맵: `/map`
- TF: `/tf`, `/tf_static`
- EKF 오도메트리: `/odometry/local`

## 기본 작업 순서
1. `teleop_launch.py` 실행
2. `slam_launch.py` 실행
3. 텔레옵으로 로봇 주행
4. RViz에서 맵 생성 확인
5. 필요 시 맵 저장

## 맵 저장 명령
맵은 아래 명령으로 저장합니다.

```bash
ros2 run nav2_map_server map_saver_cli -f ~/wego_ws/src/ranger/wego_2d_nav/maps/파일명
```

예를 들어 `office_map`으로 저장하면 아래 두 파일이 생성됩니다.
- `~/wego_ws/src/ranger/wego_2d_nav/maps/office_map.yaml`
- `~/wego_ws/src/ranger/wego_2d_nav/maps/office_map.pgm`

## 맵 저장 후 수정할 곳
새로 저장한 맵을 Navigation 기본 맵으로 쓰려면 아래 중 하나를 선택합니다.

### 방법 1. 실행할 때 map 인자로 직접 넘기기
```bash
ros2 launch wego nav2_bringup_launch.py map:=/home/user/wego_ws/src/ranger/wego_2d_nav/maps/office_map.yaml
```

### 방법 2. 기본 맵 경로 자체를 변경하기
기본 맵 경로는 아래 파일에서 설정합니다.
- `wego/launch/nav2_bringup_launch.py`

현재 기본값은 `wego_2d_nav/maps/test.yaml` 입니다.
새 맵을 기본값으로 쓰려면 `declare_map_yaml_cmd`의 `default_value`를 저장한 yaml 경로로 바꾸면 됩니다.

## 참고 사항
- SLAM은 원본 전후면 스캔이 아니라 `/scan_filtered`를 사용합니다.
- 맵 품질이 좋지 않으면 먼저 scan merger body filter와 라이다 최대 거리부터 확인하는 것이 좋습니다.
- `map`이 보이지 않으면 `slam_toolbox` 실행 상태와 `/scan_filtered` 갱신 여부를 먼저 확인해야 합니다.

## 빠른 확인 명령
```bash
ros2 topic echo /map --once
ros2 topic echo /scan_filtered --once
ros2 node list | rg "slam|ekf|vectornav|laser_scan_merger"
```
