# Navigation Manual

## 개요
Navigation bringup 기준 런치는 `wego/launch/nav2_bringup_launch.py` 입니다.

이 런치는 아래 항목을 실행합니다.
- `nav2_container`
- localization stack
- navigation stack
- 선택 사항: `rviz2`

현재 활성화된 controller plugin은 아래와 같습니다.
- `nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController`

## 실행 방법
워크스페이스 루트에서 실행합니다.

```bash
ros2 launch wego nav2_bringup_launch.py
```

RViz 없이 실행하려면:

```bash
ros2 launch wego nav2_bringup_launch.py gui_nav:=false
```

저장한 다른 맵을 바로 사용하려면 `map` 인자를 넘깁니다.

```bash
ros2 launch wego nav2_bringup_launch.py map:=/home/user/wego_ws/src/ranger/wego_2d_nav/maps/파일명.yaml
```

## 주요 파일
- 런치: `wego/launch/nav2_bringup_launch.py`
- Nav2 파라미터: `wego_2d_nav/config/nav2_params.yaml`
- Navigation launch: `wego_2d_nav/launch/navigation_launch.py`
- Localization launch: `wego_2d_nav/launch/localization_launch.py`
- RViz 설정: `wego/rviz/navigation.rviz`

## 현재 Navigation 기본값
- 기본 맵 파일: `wego_2d_nav/maps/test.yaml`
- Controller: `RPP`
- `xy_goal_tolerance`: `0.2`
- `yaw_goal_tolerance`: `0.25`
- `min_theta_velocity_threshold`: `0.01`

## 맵을 바꿀 때 수정할 곳
맵을 새로 저장한 뒤 기본 맵으로 계속 사용하려면 아래 파일을 확인합니다.
- `wego/launch/nav2_bringup_launch.py`

이 파일의 `declare_map_yaml_cmd`에서 기본 맵 경로를 설정합니다.
한 번만 시험할 때는 파일을 수정하지 말고 launch 인자로 `map:=...`를 넘기는 것이 더 안전합니다.

## 현재 Costmap에서 사용하는 Scan 설정
로컬 / 글로벌 코스트맵 모두 `/scan_filtered`를 사용합니다.

### Local costmap
- `global_frame`: `odom`
- `resolution`: `0.05`
- `width`: `5`
- `height`: `5`
- `clearing`: `True`
- `inf_is_valid`: `true`
- `observation_persistence`: `0.0`
- `obstacle_max_range`: `8.0`
- `raytrace_max_range`: `10.0`
- `always_send_full_costmap`: `True`

### Global costmap
- `global_frame`: `map`
- `resolution`: `0.1`
- `width`: `500`
- `height`: `500`
- `clearing`: `True`
- `inf_is_valid`: `true`
- `observation_persistence`: `0.0`
- `obstacle_max_range`: `18.0`
- `raytrace_max_range`: `20.0`
- `always_send_full_costmap`: `True`

## 중요 런타임 참고 사항
- Navigation은 `map -> odom -> base_link` TF 체인이 정상이어야 동작합니다.
- AMCL에 초기 자세가 없으면 `map` 프레임이 생기지 않아 Nav2가 멈춥니다.
- AMCL을 사용할 때는 RViz에서 초기 자세를 먼저 넣고 테스트하는 것이 좋습니다.

## 자주 발생하는 문제
### 1. 목표 근처에서 도착 판정이 잘 안 남
아래를 확인합니다.
- `yaw_goal_tolerance`
- 작은 `angular.z` 출력 여부
- `/cmd_vel`과 `/odometry/local` 실제 응답

### 2. RViz에서 local costmap이 비어 보임
아래를 확인합니다.
- `/local_costmap/costmap`
- RViz Fixed Frame
- `/scan_filtered`
- `local_costmap` lifecycle 상태

### 3. Costmap 잔상이 남음
현재 잔상 완화용 설정은 이미 반영되어 있습니다.
- `inf_is_valid: true`
- `observation_persistence: 0.0`
- merged scan의 빈 빔을 `+Inf`로 발행

## 빠른 확인 명령
```bash
ros2 topic info /local_costmap/costmap
ros2 topic echo /local_costmap/costmap --once
ros2 topic echo /amcl_pose --once
ros2 node list | rg "amcl|controller_server|planner_server|local_costmap|global_costmap"
```

## 시작 전 점검 순서
1. Data bringup이 살아 있는지 확인
2. `/scan_filtered`가 갱신되는지 확인
3. `/odometry/local`이 갱신되는지 확인
4. Map server가 active 상태인지 확인
5. Initial pose를 넣었는지 확인
6. `map -> odom -> base_link` TF가 정상인지 확인
