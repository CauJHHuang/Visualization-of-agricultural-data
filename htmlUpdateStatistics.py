import pymysql
from flask import Flask, request, jsonify
app = Flask(__name__)

def select_statistics(select_sql):
    """查询语句"""
    # 建立数据库连接
    db=pymysql.connect(
        host="bj-cdb-knrsiywz.sql.tencentcdb.com",
        port=6082,
        user="root",
        passwd="weizhi2017",
        db="bochuang_data",
        charset="utf8"
    )
    # 创建游标对象，并使查询结果以字典格式输出（列表嵌套字典，否则默认是元组嵌套元组）
    cur=db.cursor(cursor=pymysql.cursors.DictCursor)
    # excute()执行sql
    cur.execute(select_sql)
    # 使用fetchall()获取所有查询结果
    data=cur.fetchall()
    # 关闭游标
    cur.close()
    # 关闭数据库连接
    db.close()
    return data

@app.route("/htmlUpdataStatistics",methods=['POST'])
def update_statistics():
    """截止至当前所选日期的作业统计"""
    # statisticType=request.json.get("statisticType").strip()
    end_date=request.json.get("endDate").strip()
    # sql="SELECT * FROM job_statistic_data WHERE statisticType='{}'".format(statisticType)
    sql = "SELECT * FROM job_statistic_data WHERE statisticType='day' AND statisticDate between '20190101'  "+"AND {}".format(end_date)
    res=select_statistics(sql)
    return(jsonify(res)) #



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1000,debug=True)  # 默认的port5000不能用，已被其他占用。