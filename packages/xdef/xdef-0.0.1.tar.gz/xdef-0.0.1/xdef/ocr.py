from .utils import *
import cv2
from PIL import Image, ImageDraw, ImageFont
from copy import deepcopy


def json2label(lines, add_path=None):
    new_lines = []
    for line in lines:
        img_path, label = line.strip().split('\t')
        if add_path is not None:
            img_path = osp.join(add_path, img_path)
        new_lines.append([img_path, json.loads(label)])
    return new_lines


def label2json(lines):
    new_lines = []
    for img_path, label in lines:
        new_line = '{}\t{}\n'.format(img_path, json.dumps(label, ensure_ascii=False))
        new_lines.append(new_line)
    return new_lines


def read_label_file(file_path):
    lines = open(file_path).read().splitlines()
    return json2label(lines)


def bbox2points(bbox):
    left, top, right, bottom = bbox
    return [[left, top], [right, top], [right, bottom], [left, bottom]]


def points2bbox(points):
    left, top = np.min(points, 0)
    right, bottom = np.max(points, 0)
    return [left, top, right, bottom]


def poly2points(points):
    x = cv2.boxPoints(cv2.minAreaRect(np.array(points, dtype='float32')))
    points = re_order(x)
    return points


def resize_img(img, input_size=600):
    """
    resize img and limit the longest side of the image to input_size
    """
    img = np.array(img)
    im_shape = img.shape
    im_size_max = np.max(im_shape[0:2])
    im_scale = float(input_size) / float(im_size_max)
    img = cv2.resize(img, None, None, fx=im_scale, fy=im_scale)
    return img


def re_order(points):
    try:
        new_points = re_order_func(points, 0)
        if new_points[1][1] >= new_points[2][1] or new_points[0][1] >= new_points[3][1]:
            try:
                new_points = re_order_func(points, 1)
            except Exception as e:
                print('Can not reorder', e)
                return points
    except:
        try:
            new_points = re_order_func(points, 1)
        except Exception as e:
            print('Can not reorder', e)
            return points
    return new_points


def re_order_func(points, axis):
    if not isinstance(points, list):
        points = points.tolist()
    points.sort(key=lambda x: x[axis])
    p1 = points[:2]
    p2 = points[2:]
    p1.sort(key=lambda x: x[1 - axis])
    p2.sort(key=lambda x: x[1 - axis])
    if axis == 1:
        points = [p1[0], p1[1], p2[1], p2[0]]
    elif axis == 0:
        points = [p1[0], p2[0], p2[1], p1[1]]
    return points


def get_rotate_crop_image(img, points):
    points = np.array(points, dtype='float32')
    assert len(points) == 4, "shape of points must be 4*2"
    img_crop_width = int(
        max(
            np.linalg.norm(points[0] - points[1]),
            np.linalg.norm(points[2] - points[3])))
    img_crop_height = int(
        max(
            np.linalg.norm(points[0] - points[3]),
            np.linalg.norm(points[1] - points[2])))
    pts_std = np.float32([[0, 0], [img_crop_width, 0],
                          [img_crop_width, img_crop_height],
                          [0, img_crop_height]])
    M = cv2.getPerspectiveTransform(points, pts_std)
    dst_img = cv2.warpPerspective(
        img,
        M, (img_crop_width, img_crop_height),
        borderMode=cv2.BORDER_REPLICATE,
        flags=cv2.INTER_CUBIC)
    # dst_img_height, dst_img_width = dst_img.shape[0:2]
    # if dst_img_height * 1.0 / dst_img_width >= 1.5:
    #     dst_img = np.rot90(dst_img)
    return dst_img


def draw_ocr(image,
             boxes,
             txts=None,
             scores=None,
             drop_score=0.5,
             font_path="./simfang.ttf"):
    """
    Visualize the results of OCR detection and recognition
    args:
        image(Image|array): RGB image
        boxes(list): boxes with shape(N, 4, 2)
        txts(list): the texts
        scores(list): txxs corresponding scores
        drop_score(float): only scores greater than drop_threshold will be visualized
        font_path: the path of font which is used to draw text
    return(array):
        the visualized img
    """
    if scores is None:
        scores = [1] * len(boxes)
    box_num = len(boxes)
    for i in range(box_num):
        if scores is not None and (scores[i] < drop_score or
                                   math.isnan(scores[i])):
            continue
        box = np.reshape(np.array(boxes[i]), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True, (255, 0, 0), 2)
    if txts is not None:
        img = np.array(resize_img(image, input_size=600))
        txt_img = text_visual(
            txts,
            scores,
            img_h=img.shape[0],
            img_w=600,
            threshold=drop_score,
            font_path=font_path)
        img = np.concatenate([np.array(img), np.array(txt_img)], axis=1)
        return img
    return image


def str_count(s):
    """
    Count the number of Chinese characters,
    a single English character and a single number
    equal to half the length of Chinese characters.
    args:
        s(string): the input of string
    return(int):
        the number of Chinese characters
    """
    import string
    count_zh = count_pu = 0
    s_len = len(s)
    en_dg_count = 0
    for c in s:
        if c in string.ascii_letters or c.isdigit() or c.isspace():
            en_dg_count += 1
        elif c.isalpha():
            count_zh += 1
        else:
            count_pu += 1
    return s_len - math.ceil(en_dg_count / 2)


def text_visual(texts,
                scores,
                img_h=400,
                img_w=600,
                threshold=0.,
                font_path="./simfang.ttf"):
    """
    create new blank img and draw txt on it
    args:
        texts(list): the text will be draw
        scores(list|None): corresponding score of each txt
        img_h(int): the height of blank img
        img_w(int): the width of blank img
        font_path: the path of font which is used to draw text
    return(array):
    """
    if scores is not None:
        assert len(texts) == len(
            scores), "The number of txts and corresponding scores must match"

    def create_blank_img():
        blank_img = np.ones(shape=[img_h, img_w], dtype=np.int8) * 255
        blank_img[:, img_w - 1:] = 0
        blank_img = Image.fromarray(blank_img).convert("RGB")
        draw_txt = ImageDraw.Draw(blank_img)
        return blank_img, draw_txt

    blank_img, draw_txt = create_blank_img()

    font_size = 20
    txt_color = (0, 0, 0)
    font = ImageFont.truetype(font_path, font_size, encoding="utf-8")

    gap = font_size + 5
    txt_img_list = []
    count, index = 1, 0
    for idx, txt in enumerate(texts):
        index += 1
        if scores[idx] < threshold or math.isnan(scores[idx]):
            index -= 1
            continue
        first_line = True
        while str_count(txt) >= img_w // font_size - 4:
            tmp = txt
            txt = tmp[:img_w // font_size - 4]
            if first_line:
                new_txt = str(index) + ': ' + txt
                first_line = False
            else:
                new_txt = '    ' + txt
            draw_txt.text((0, gap * count), new_txt, txt_color, font=font)
            txt = tmp[img_w // font_size - 4:]
            if count >= img_h // gap - 1:
                txt_img_list.append(np.array(blank_img))
                blank_img, draw_txt = create_blank_img()
                count = 0
            count += 1
        if first_line:
            new_txt = str(index) + ': ' + txt + '   ' + '%.3f' % (scores[idx])
        else:
            new_txt = "  " + txt + "  " + '%.3f' % (scores[idx])
        draw_txt.text((0, gap * count), new_txt, txt_color, font=font)
        # whether add new blank img or not
        if count >= img_h // gap - 1 and idx + 1 < len(texts):
            txt_img_list.append(np.array(blank_img))
            blank_img, draw_txt = create_blank_img()
            count = 0
        count += 1
    txt_img_list.append(np.array(blank_img))
    if len(txt_img_list) == 1:
        blank_img = np.array(txt_img_list[0])
    else:
        blank_img = np.concatenate(txt_img_list, axis=1)
    return np.array(blank_img)


def order_by_tbyx(ocr_info, th=20):
    """
    ocr_info: a list of dict, which contains bbox information([x1, y1, x2, y2])
    th: threshold of the position threshold
    """
    res = sorted(ocr_info, key=lambda r: (r["bbox"][1], r["bbox"][0]))  # sort using y1 first and then x1
    for i in range(len(res) - 1):
        for j in range(i, 0, -1):
            # restore the order using the
            if abs(res[j + 1]["bbox"][1] - res[j]["bbox"][1]) < th and \
                    (res[j + 1]["bbox"][0] < res[j]["bbox"][0]):
                tmp = deepcopy(res[j])
                res[j] = deepcopy(res[j + 1])
                res[j + 1] = deepcopy(tmp)
            else:
                break
    return res


def draw_det_boxes(lines_or_label_file, output_dir='tmp'):
    if isinstance(lines_or_label_file, str):
        lines = read_label_file(lines_or_label_file)
    else:
        lines = lines_or_label_file

    for line in lines:
        img_path, label = line
        boxes = [x['points'] for x in label]
        draw_det_res(boxes, img_path, output_dir)


def draw_det_res(dt_boxes, img, save_path):
    if isinstance(img, str):
        img_name = osp.basename(img)
        img = cv2.imread(img)
    src_im = img
    for box in dt_boxes:
        # print(box)
        box = np.array(box).astype(np.int32).reshape((-1, 1, 2))
        cv2.polylines(src_im, [box], True, color=(255, 255, 0), thickness=2)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_path = os.path.join(save_path, os.path.basename(img_name))
    cv2.imwrite(save_path, src_im)


if __name__ == '__main__':
    x = [[304, 122], [308, 76], [307, 76], [305, 122]]
    print(re_order_func(x, 0))
    print(re_order_func(x, 1))
    print(re_order(x))

    x = [[107, 349], [701, 319], [702, 346], [106, 371]]
    print(re_order_func(x, 0))
    print(re_order_func(x, 1))
    print(re_order(x))
