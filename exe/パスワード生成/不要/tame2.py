import PySimpleGUI as sg
from PIL import Image, ImageTk
import io

#先程確認して決めたテーマカラーを設定
sg.theme('SystemDefaultForReal')

"""
公式のサンプル集に乗ってたコードをそのまま引用
maxsizeを大きくすると、大きな画像を読み込んだ際にGUIがその分大きくなる
今回はフレームサイズ以下になるように、450×450を表示最大サイズとした
"""
def get_img_data(f, maxsize=(450, 450), first=False):
    """画像を読み込む関数"""
    global status_text #画像サイズをGUI表示させるためにグローバル変数で関数外でも参照できるようにする
    img = Image.open(f)
    status_text = "%d x %d" % img.size  # オリジナルの画像サイズ
    img.thumbnail(maxsize) #アスペクト比を維持しながら、指定したサイズ以下の画像に縮小
    status_text += " (%d x %d)" % img.size  # 縮小された画像サイズ
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

#GUIへ初期画像を登録する(適当にパワポとかで作っておけばいい)
fname_first = './IMG_3334-1-1280x960.jpg'
image_elem = sg.Image(data=get_img_data(fname_first, first=True))

#画像サイズを表示させる部分を変数化しておく(画像毎にアップデートさせるため)
status_elem = sg.Text(key='-STATUS-', size=(64, 1))

"""
・sg.Imageで画像部品をのせられる
・sg.Textでテキスト部品をのせられる
・sg.InputTextでテキスト入力エリアをのせる(画像Pathを表示させる部分)
・sg.FileBrowseでWindowsでよく見るファイル選択画面を出せる(InputTextの横に置けばtextを自動入力してくれる)
・sg.Submitはいわゆる「決定ボタン」。今回はOCR開始ボタンとして使った
・sg.MLineはテキスト出力エリア
・keyは、後でイベントを追加する時に参照する変数名
・後は省略できるが、サイズやフォントも各命令で指定出来る
"""
#フレーム1
frame1 = sg.Frame('',
    [
        # テキストレイアウト
        [
            sg.Text('①画像選択ボタンを押してOCRを行いたい画像を選んでね', font=('メイリオ',12))
        ],
        #画像選択ボタン ※3つカンマ区切りで書いてるのでこれらが同じ行に配置される
        [
            sg.Text("ファイル"),
            sg.InputText('ファイルを選択', key='-INPUTTEXT-', enable_events=True,), 
            sg.FileBrowse(button_text='画像選択', font=('メイリオ',8), size=(8,3), key="-FILENAME-")
        ],
        # テキストレイアウト
        [
            sg.Text("②画像を選択したらOCR開始ボタンを押してね", font=('メイリオ',12)),
        ],
        #画像サイズ表示
        [
            sg.Text("元画像サイズ(GUI表示画像サイズ) : "),
            status_elem #
        ],
        #画像表示 ※初期画面では自分で用意した適当な画像を表示
        [
            image_elem,
        ],
        #OCR開始ボタン
        [
            sg.Submit(button_text='OCR開始',
                      font=('メイリオ',8),size=(8,3),key='button_ocr')
        ]
    ], size=(500, 700)
)

#フレーム2
frame2 = sg.Frame('',
    [
        # テキストレイアウト
        [
            sg.Text("OCR結果"), 
        ],
        # MLineでテキストエリアを作成。sizeは「**列×**行」を表している
        [
            sg.MLine(font=('メイリオ',8), size=(50,60), key='-OUTPUT-'),
        ]
    ] , size=(400, 700)
)

#左と右のフレームを合体させた全体レイアウト
layout = [
    [
        frame1,
        frame2
    ]
]

#GUIタイトルと全体レイアウトをのせたWindowを定義する
window = sg.Window('日本語OCR実行アプリ', layout, resizable=True)

#GUI表示実行部分
while True:
    # ウィンドウ表示
    event, values = window.read()

    #クローズボタンの処理
    if event is None:
        print('exit')
        break

window.close()