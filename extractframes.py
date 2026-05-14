import cv2
import os
import textwrap

def crop_black_bars(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    coords = cv2.findNonZero(thresh)
    if coords is None:
        return frame
    x, y, w, h = cv2.boundingRect(coords)
    return frame[y:y+h, x:x+w]

def cover_burned_subs(frame):
    h = frame.shape[0]
    sub_region = frame[int(h * 0.78):, :]
    frame[int(h * 0.78):, :] = cv2.GaussianBlur(sub_region, (51, 51), 0)
    return frame

def draw_speech_bubble(frame, text, font=cv2.FONT_HERSHEY_DUPLEX, font_scale=0.8, thickness=1):
    if not text.strip():
        return frame
    h, w = frame.shape[:2]
    char_w = cv2.getTextSize('W', font, font_scale, thickness)[0][0]
    max_chars = max(10, int(w * 0.9 / char_w))
    lines = textwrap.wrap(text, width=max_chars) or [text]

    line_h = cv2.getTextSize('Ag', font, font_scale, thickness)[0][1]
    pad = 10
    bubble_w = max(cv2.getTextSize(l, font, font_scale, thickness)[0][0] for l in lines) + pad * 2
    bubble_h = line_h * len(lines) + pad * 2 + (len(lines) - 1) * 6
    bx = (w - bubble_w) // 2
    by = h - bubble_h - 20

    overlay = frame.copy()
    cv2.rectangle(overlay, (bx - 4, by - 4), (bx + bubble_w + 4, by + bubble_h + 4), (0, 0, 0), -1)
    cv2.rectangle(overlay, (bx, by), (bx + bubble_w, by + bubble_h), (255, 255, 255), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

    for i, line in enumerate(lines):
        ty = by + pad + line_h + i * (line_h + 6)
        tx = bx + pad
        cv2.putText(frame, line, (tx, ty), font, font_scale, (0, 0, 0), thickness + 1, cv2.LINE_AA)
        cv2.putText(frame, line, (tx, ty), font, font_scale, (20, 20, 20), thickness, cv2.LINE_AA)
    return frame

def extract_frame(video_path, start_time, end_time, count, div=2, dialogue=[''], frames_dir='frames'):
    os.makedirs(frames_dir, exist_ok=True)
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)

    start_minutes, start_seconds = map(int, start_time.split(':'))
    end_minutes, end_seconds = map(int, end_time.split(':'))

    start_frame = int((start_minutes * 60 + start_seconds) * fps)
    end_frame = int((end_minutes * 60 + end_seconds) * fps)

    for i in range(1, div):
        frame_number = start_frame + ((end_frame - start_frame) * (i / div))
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        res, frame = video.read()
        if res:
            frame = crop_black_bars(frame)
            frame = cover_burned_subs(frame)
            frame = draw_speech_bubble(frame, dialogue[i-1])
            cv2.imwrite(os.path.join(frames_dir, f'frame{count}.jpg'), frame)
            count += 1

    video.release()
    return count