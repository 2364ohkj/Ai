import cv2
import os
import numpy as np

def stabilize_frames(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # ----------------------------
    # 1) 입력 파일 정렬
    # ----------------------------
    files = sorted(os.listdir(input_dir))
    paths = [os.path.join(input_dir, f)
             for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if len(paths) < 2:
        print("⚠️ 안정화할 프레임이 부족합니다 (2개 이상 필요)")
        return input_dir

    # ----------------------------
    # 2) 첫 프레임을 기준으로 크기 결정
    # ----------------------------
    first_img = cv2.imread(paths[0])
    H, W = first_img.shape[:2]

    prev_img = cv2.resize(first_img, (W, H))
    prev_gray = cv2.cvtColor(prev_img, cv2.COLOR_BGR2GRAY)

    transforms = []

    # ----------------------------
    # 3) Optical Flow 기반 이동 추정
    # ----------------------------
    for i in range(1, len(paths)):
        curr_img = cv2.imread(paths[i])
        curr_img = cv2.resize(curr_img, (W, H))  # 강제 동일 크기
        curr_gray = cv2.cvtColor(curr_img, cv2.COLOR_BGR2GRAY)

        # Optical Flow 포인트
        pts_prev = cv2.goodFeaturesToTrack(prev_gray,
                                           maxCorners=300,
                                           qualityLevel=0.01,
                                           minDistance=20,
                                           blockSize=3)

        if pts_prev is None or len(pts_prev) < 10:
            print(f"⚠️ Optical Flow 포인트 부족 → 프레임 {i} identity transform")
            m = np.array([[1, 0, 0],
                          [0, 1, 0]])
            transforms.append(m)
            prev_gray = curr_gray
            continue

        pts_curr, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, pts_prev, None)

        # 유효 포인트만 선택
        idx = st.reshape(-1) == 1
        pts_prev = pts_prev[idx]
        pts_curr = pts_curr[idx]

        if len(pts_prev) < 10:
            print(f"⚠️ Optical Flow 유효 포인트 부족 → 프레임 {i} identity transform")
            m = np.array([[1, 0, 0],
                          [0, 1, 0]])
            transforms.append(m)
            prev_gray = curr_gray
            continue

        # 이동 변환 행렬 추정 (Affine with only shift + scale)
        m, _ = cv2.estimateAffinePartial2D(pts_prev, pts_curr)

        # 실패하면 identity
        if m is None:
            m = np.array([[1, 0, 0],
                          [0, 1, 0]])

        transforms.append(m)
        prev_gray = curr_gray

    # ----------------------------
    # 4) 실제 안정화 적용
    # ----------------------------
    stabilized_paths = []

    # 첫 프레임 저장
    out_path0 = os.path.join(output_dir, files[0])
    cv2.imwrite(out_path0, first_img)
    stabilized_paths.append(out_path0)

    # 나머지 프레임 안정화
    for i in range(1, len(paths)):
        img = cv2.imread(paths[i])
        img = cv2.resize(img, (W, H))  # 크기 강제 통일

        m = transforms[i - 1]

        stabilized = cv2.warpAffine(
            img, m, (W, H),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT
        )

        out_path = os.path.join(output_dir, files[i])
        cv2.imwrite(out_path, stabilized)
        stabilized_paths.append(out_path)

    return output_dir
