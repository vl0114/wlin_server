from flask import Flask, render_template, abort
import wlin_server

app = Flask(__name__)
w = wlin_server.WLinServer()


@app.route('/')
def client_list():

    return render_template('connected_client_list.html', client_list=w.wl_client_list)


@app.route('/stat/<name>')
def client_stat(name):
    c = None
    for i in w.wl_client_list:
        if i.name == name:
            c = i
            break
    if c is None:
        abort(404)
    else:
        x = c.get_proc_stat()
        print(x)
        mem_usage = (int(c.get_mem_stat()["total"]) - int(c.get_mem_stat()["free"])) / int(c.get_mem_stat()["total"]) * 100
        swap_usage = (int(c.get_mem_stat()["total_swap"]) - int(c.get_mem_stat()["free_swap"])) / int(c.get_mem_stat()["total_swap"]) * 100
        return render_template('client_stat.html', client_info=c, mu=mem_usage, su=swap_usage)
if __name__ == '__main__':

    app.run(host='0.0.0.0')

    w._t.join()


