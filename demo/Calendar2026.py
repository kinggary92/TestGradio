# instance/page1.py
import gradio as gr

def build():
    html_str = """
    <style>
        /* 隐藏 radio */
        .month-radio {
            position: absolute;
            left: -9999px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
        }

        /* ===== 标题 ===== */
        .header {
            text-align: center;
            margin-bottom: 16px;
        }

        .header h1 {
            font-size: 30px;
            font-weight: 700;
            color: #111827;
            margin: 0;
        }

        /* ===== 月份选择 ===== */
        .month-selector {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }

        .month-btn {
            padding: 6px 12px;
            border-radius: 8px;
            border: 1px solid #d1d5db;
            background: #f9fafb;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            color: #374151;
            user-select: none;
        }

        .month-btn:hover {
            background: #e5e7eb;
        }

        #m1:checked ~ .month-selector label[for="m1"],
        #m2:checked ~ .month-selector label[for="m2"],
        #m3:checked ~ .month-selector label[for="m3"],
        #m4:checked ~ .month-selector label[for="m4"],
        #m5:checked ~ .month-selector label[for="m5"],
        #m6:checked ~ .month-selector label[for="m6"],
        #m7:checked ~ .month-selector label[for="m7"],
        #m8:checked ~ .month-selector label[for="m8"],
        #m9:checked ~ .month-selector label[for="m9"],
        #m10:checked ~ .month-selector label[for="m10"],
        #m11:checked ~ .month-selector label[for="m11"],
        #m12:checked ~ .month-selector label[for="m12"] {
            background: #2563eb;
            color: #ffffff;
            border-color: #2563eb;
        }

        /* ===== 星期 ===== */
        .week {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            text-align: center;
            font-weight: 600;
            color: #6b7280;
            margin-bottom: 12px;
        }

        /* ===== 日历 ===== */
        .calendar {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 12px;
        }

        .day, .empty {
            min-height: 110px;
            border-radius: 12px;
        }

        .day {
            border: 1px solid #e5e7eb;
            padding: 8px;
            background: #fff;
        }

        .day:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        }

        .num {
            font-weight: 600;
            margin-bottom: 6px;
        }

        .event {
            display: block;
            margin-top: 6px;
            padding: 4px 8px;
            font-size: 12px;
            color: white;
            border-radius: 6px;
            text-decoration: none;
        }

        .blue { background: #3b82f6; }
        .green { background: #10b981; }

        .empty {
            background: #f9fafb;
        }

        /* ===== 月份内容切换 ===== */
        .month { display: none; }

        #m1:checked ~ .content .m1,
        #m2:checked ~ .content .m2 {
            display: block;
        }
    </style>

    <div class="container">

        <!-- 月份状态 -->
        <input class="month-radio" type="radio" name="m" id="m1">
        <input class="month-radio" type="radio" name="m" id="m2" checked>
        <input class="month-radio" type="radio" name="m" id="m3">
        <input class="month-radio" type="radio" name="m" id="m4">
        <input class="month-radio" type="radio" name="m" id="m5">
        <input class="month-radio" type="radio" name="m" id="m6">
        <input class="month-radio" type="radio" name="m" id="m7">
        <input class="month-radio" type="radio" name="m" id="m8">
        <input class="month-radio" type="radio" name="m" id="m9">
        <input class="month-radio" type="radio" name="m" id="m10">
        <input class="month-radio" type="radio" name="m" id="m11">
        <input class="month-radio" type="radio" name="m" id="m12">

        <!-- 标题 -->
        <div class="header">
            <h1>2026 年 AI 热点信息</h1>
        </div>

        <!-- 月份选择 -->
        <div class="month-selector">
            <label for="m1" class="month-btn">1 月</label>
            <label for="m2" class="month-btn">2 月</label>
            <label for="m3" class="month-btn">3 月</label>
            <label for="m4" class="month-btn">4 月</label>
            <label for="m5" class="month-btn">5 月</label>
            <label for="m6" class="month-btn">6 月</label>
            <label for="m7" class="month-btn">7 月</label>
            <label for="m8" class="month-btn">8 月</label>
            <label for="m9" class="month-btn">9 月</label>
            <label for="m10" class="month-btn">10 月</label>
            <label for="m11" class="month-btn">11 月</label>
            <label for="m12" class="month-btn">12 月</label>
        </div>

        <!-- 星期 -->
        <div class="week">
            <div>周一</div><div>周二</div><div>周三</div>
            <div>周四</div><div>周五</div><div>周六</div><div>周日</div>
        </div>

        <!-- 内容 -->
        <div class="content">

            <div class="month m1">
                <div class="calendar">
                    <div class="empty"></div><div class="empty"></div><div class="empty"></div>
                    <div class="day"><div class="num">1</div></div>
                    <div class="day"><div class="num">2</div></div>
                    <div class="day"><div class="num">3</div></div>
                    <div class="day"><div class="num">4</div></div>
                    <div class="day">
                        <div class="num">5</div>
                        <a href="/test/a" class="event blue">CES 展会洞察</a>
                    </div>
                </div>
            </div>

            <div class="month m2">
                <div class="calendar">
                    <div class="empty"></div><div class="empty"></div><div class="empty"></div>
                    <div class="empty"></div><div class="empty"></div><div class="empty"></div>
                    <div class="day">
                        <div class="num">1</div>
                        <a href="/test/b" class="event green">春节技术专题</a>
                    </div>
                </div>
            </div>

        </div>

    </div>
    """
    gr.HTML(html_str)