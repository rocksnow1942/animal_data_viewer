from flask import Flask
import os, json, pathlib
from flask import render_template, flash, request, jsonify, send_from_directory,redirect,url_for

# config = {
# 'ANIMAL_DATA_PATH': "/Users/hui/Aptitude_Cloud/Project Management/AnimalResultServer",
# 'JSON_FILE_PATH' : "/Users/hui/desktop/hui-mk-data"
# }


class CONFIG(dict):
    _save_path = os.path.join(os.path.dirname(__file__), 'settings.json')
    def __init__(self,):
        with open(self._save_path, 'rt') as f:
            config = json.load(f)
        super().__init__(**config)

    def save(self):
        with open(self._save_path, 'wt') as f:
            json.dump(self,f,indent=2)


class Experiment(object):
    """
    init the class with folder path to experiment results 
    folder structure needs to be:
    -Experiment name 
     |-D5
       |-FP
       |- Monkey 
          |- XXXXXXX-L.jpg
          |- XXXXXXX-R.jpg
       |-OCT
       |- Monkey 
          |-OD 
            |- XXXXXX.jpg
    """
    def __init__(self, path, savepath):
        """
        init the instance and save json file automatically.
        """
        self.path = path
        pa = pathlib.Path(path)
        self.savepath = savepath
        self.note = ""
        self.data = {}
        self.init_data()
        self.save_json()

    def save_json(self):
        with open(self.savepath + '.json', 'wt') as f:
            json.dump(self.__dict__, f, separators=(',', ':'))

    @classmethod
    def load_json(cls, file, datapath):
        """
        file is json file location,
        datapath is animal data image file folder path. 
        use datapath to update json file's path attribute, so that it can properly update empty files. 
        """
        with open(file, 'rt') as f:
            data = json.load(f)
        new = cls.__new__(cls)
        new.__dict__ = data
        # each time loading, set the file and folder path again; incase file is being loaded on different systems.
        pa = pathlib.Path(file)
        new.savepath = str(pa.parent / pa.stem)
        datapath = pathlib.Path(datapath)
        new.path = str(datapath / pa.stem)
        return new

    def update(self):
        needupdate = self.init_data(update=True)
        needupdate = self.remove_dead_files() or needupdate
        if needupdate:
            self.remove_empty_data()
            self.save_json()

    def remove_dead_files(self):
        needupdate = False
        todelete = []
        for l1, monkey in self.data.items():
            for l2, eye in monkey.items():
                for l3, measure in eye.items():
                    if l3 in ('FP', 'OCT'):
                        for l4, days in measure.items():
                            newdays = [
                                i for i in days
                                if os.path.isfile(os.path.join(self.path, i))
                            ]
                            if newdays != days:
                                needupdate = True
                                self.data[l1][l2][l3][l4] = newdays
        return needupdate

    def remove_empty_data(self):
        """
        remove empty monkey or eye or measure or day dictionary
        avoids dead link options. 
        """
        days = [i for i in self.day_iterator() if not self.get_item(*i)]
        for d in days:
            self.get_item(*d[:-1]).pop(d[-1])

        measures = [
            i for i in self.measure_iterator() if not self.get_item(*i)
        ]
        for m in measures:
            self.get_item(*m[:-1]).pop(m[-1])
        eyes = [
            i for i in self.eye_iterator()
            if (('FP' not in self.get_item(*i).keys()) and (
                'OCT' not in self.get_item(*i).keys()))
        ]
        for e in eyes:
            self.get_item(*e[:-1]).pop(e[-1])
        monkeys = [i for i in self.monkey_iterator() if not self.get_item(i)]
        for m in monkeys:
            self.data.pop(m)

    def get_item(self, *args):
        result = self.data
        for i in args:
            result = result.get(i)
        return result

    def day_iterator(self):
        for l1, monkey in self.data.items():
            for l2, eye in monkey.items():
                for l3, measure in eye.items():
                    if l3 in ('FP', 'OCT'):
                        for l4, days in measure.items():
                            yield l1, l2, l3, l4

    def measure_iterator(self):
        for l1, monkey in self.data.items():
            for l2, eye in monkey.items():
                for l3, measure in eye.items():
                    if l3 in ('FP', 'OCT'):
                        yield l1, l2, l3

    def eye_iterator(self):
        for l1, monkey in self.data.items():
            for l2, eye in monkey.items():
                yield l1, l2

    def monkey_iterator(self):
        yield from self.data.keys()

    def getitem(self, *args):
        result = self.data
        for i in args:
            result = result.get(i)
        return result

    def update_entry(self, monkey, eye, measure, day, data):
        need_update = True
        if self.data.get(monkey, None) is None:
            self.data[monkey] = {}
        if self.data[monkey].get(eye, None) is None:
            self.data[monkey][eye] = {'note': ""}
        if self.data[monkey][eye].get(measure, None) is None:
            self.data[monkey][eye][measure] = {}
        if self.data[monkey][eye][measure].get(day, None) is None:
            self.data[monkey][eye][measure][day] = data  # create new data
        else:
            if set(data) == set(self.data[monkey][eye][measure][day]):
                need_update = False
            else:
                self.data[monkey][eye][measure][
                    day] = data  # if day is already there, decide if need to update.
        return need_update

    def create_entry(self, monkey, eye, measure, day, data):
        if self.data.get(monkey, None) is None:
            self.data[monkey] = {}
        if self.data[monkey].get(eye, None) is None:
            self.data[monkey][eye] = {'note': "", 'FP': {}, 'OCT': {}}

        self.data[monkey][eye][measure][day] = data

    def init_data(self, update=False):
        homedir = pathlib.Path(self.path)
        need_update = not update
        for root, folder, files in os.walk(self.path):
            pa = pathlib.Path(root)
            pa_parts = pa.parts
            if pa_parts[-2] == 'FP':
                monkey = pa_parts[-1]
                day = pa_parts[-3]
                L = [i for i in files if i.endswith('L.jpg')]
                R = [i for i in files if i.endswith('R.jpg')]
                L.sort(), R.sort()
                relative = pa.relative_to(homedir)
                L = [os.path.join(relative, i) for i in L]
                R = [os.path.join(relative, i) for i in R]
                if update:
                    need_update = self.update_entry(monkey, 'L', 'FP', day, L)
                    need_update = self.update_entry(monkey, 'R', 'FP', day, R)
                else:
                    self.create_entry(monkey, 'L', 'FP', day, L)
                    self.create_entry(monkey, 'R', 'FP', day, R)

            elif pa_parts[-3] == 'OCT':
                monkey = pa_parts[-2]
                day = pa_parts[-4]
                eye = pa_parts[-1]
                relative = pa.relative_to(homedir)
                eye = {'OD': 'R', 'OS': 'L'}[eye]
                data = [i for i in files if i.endswith('.jpg')]
                data.sort()
                data = [os.path.join(relative, i) for i in data]
                if update:
                    need_update = self.update_entry(monkey, eye, 'OCT', day,
                                                    data)
                else:
                    self.create_entry(monkey, eye, 'OCT', day, data)
        return need_update

    def list_animal(self):
        return list(self.data.keys())

    def render_form_kw(self, data):
        exp = data.get('exp', '')
        exp_animal = sorted(list(self.data.keys()))
        animal = data.get('animal', exp_animal[0])
        exp_eye = sorted([i for i in self.data.get(animal, {}).keys()])
        eye = data.get('eye', exp_eye[0])
        exp_measure = sorted([
            i for i in self.data.get(animal, {}).get(eye, {}).keys()
            if i != 'note'
        ])
        exp_note = self.data.get(animal, {}).get(eye, {}).get('note', '')
        measure = data.get('measure', exp_measure[0])
        exp_day = sorted([
            i for i in self.data.get(animal, {}).get(eye, {}).get(measure,
                                                                  {}).keys()
        ])
        day = data.get('day', exp_day and exp_day[0])
        return dict(exp_animal=exp_animal,
                    exp_eye=exp_eye,
                    exp_measure=exp_measure,
                    exp_note=exp_note,
                    exp_day=exp_day,
                    exp=exp,
                    animal=animal,
                    eye=eye,
                    measure=measure,
                    day=day)

    def render_figure_kw(self, data):
        exp = data.get('exp')
        animal = data.get('animal', )
        eye = data.get('eye', )
        measure = data.get('measure', )
        day = data.get('day', )
        return [
            os.path.join(exp, i) for i in self.data[animal][eye][measure][day]
        ]

    def edit_data(self, data, order):
        exp = data.get('exp')
        animal = data.get('animal', )
        eye = data.get('eye', )
        measure = data.get('measure', )
        day = data.get('day', )
        self.data.get(animal, {}).get(eye, {})['note'] = data.get('note')
        old = self.data[animal][eye][measure][day]
        if len(order) == len(old):
            self.data[animal][eye][measure][day] = [old[i] for i in order]
        return f"{exp}-{animal}-{eye}"


config=CONFIG()



app = Flask(__name__)
app.config['SECRET_KEY']='a smart secret key,you cannot guess.'

@app.route('/', methods=['GET', 'POST'])
def index():
    if not request.args:
        datapath = config.get('ANIMAL_DATA_PATH',"") or "/Users/Aptitude_Cloud/Project Management/AnimalResultServer"
        jsonpath = config.get('JSON_FILE_PATH', "") or str(pathlib.Path(os.path.abspath(__file__)).parent/'experiment_index')
        if not os.path.isdir(pathlib.Path(os.path.abspath(__file__)).parent/'experiment_index'):
            os.mkdir(str(pathlib.Path(os.path.abspath(__file__)).parent/'experiment_index'))

    else:
        datapath = request.args.get('datapath').strip()
        jsonpath = request.args.get('jsonpath').strip()
        invalid = []
        if not os.path.isdir(datapath): invalid.append(datapath)
        if not os.path.isdir(jsonpath): invalid.append(jsonpath)
        if not invalid:
            config['ANIMAL_DATA_PATH'] = datapath
            config['JSON_FILE_PATH'] =jsonpath
            config.save()
            return redirect(url_for('animal_data'))
        else:
            mmm = " and ".join([f"<'{i}'>" for i in invalid])
            flash(f'File path {mmm} not valid.','warning')
    return render_template('index.html',datapath=datapath,jsonpath=jsonpath)

@app.route('/animal_data', methods=['GET', 'POST'])
def animal_data():
    data_path = config['ANIMAL_DATA_PATH']
    json_path = config['JSON_FILE_PATH']
    filelist = os.listdir(data_path)
    experimentlist = [i.replace('.json','') for i in os.listdir(json_path) if i.endswith('.json')]
    for i in filelist:
        if os.path.isdir(os.path.join(data_path, i)) and (i not in experimentlist):
            try:
                Experiment(os.path.join(data_path, i),os.path.join(json_path, i))
                experimentlist.append(i)
            except Exception as e:
                flash('Experiment {} cannot be loaded. Reason:{}'.format(i,e), 'warning')
    return render_template('animal/animal_data.html', title= "Animal Data Viewer",experiment_list=experimentlist)


@app.route('/animal_data_form', methods=['POST'])
def animal_data_form():
    data_path = config['ANIMAL_DATA_PATH']
    json_path = config['JSON_FILE_PATH']
    data = {item['name']: item['value'] for item in request.json}
    messages=None
    render_kw = {}
    try:
        if data['exp'].strip():
            exp = Experiment.load_json(os.path.join(json_path,data['exp'].strip()+'.json'),data_path)
            exp.update()
            render_kw = exp.render_form_kw(data)
    except Exception as e:
        messages = render_template('flash_messages.html', messages=[
            ('warning', f"Loading error: {e}")])
    form = render_template('animal/animal_data_form.html', **render_kw)
    title = f"{render_kw.get('animal')}-{render_kw.get('eye')}-{render_kw.get('measure')}-{render_kw.get('day')}"
    return jsonify(form=form,title=title,msg=messages)


@app.route('/animal_data_figure', methods=['POST'])
def animal_data_figure():
    data_path = config['ANIMAL_DATA_PATH']
    json_path = config['JSON_FILE_PATH']
    data = {item['name']: item['value'] for item in request.json}
    try:
        exp = Experiment.load_json(
            os.path.join(json_path, data['exp'] + '.json'),data_path)
        figure_list = exp.render_figure_kw(data)
        note = exp.data.get(data['animal'], {}).get(data['eye'], {}).get('note', '')
    except Exception as e:
        figure_list = {}
        note=''
    html = render_template('animal/animal_data_figure.html', figure_list = figure_list)
    return jsonify(html=html, note=note )


@app.route('/save_animal_data', methods=['POST'])
def save_animal_data():
    data_path = config['ANIMAL_DATA_PATH']
    json_path = config['JSON_FILE_PATH']
    try:
        data = {item['name']: item['value']
                for item in request.json.get('data')}
        order = [int(i) for i in request.json.get('order')]
        exp = Experiment.load_json(
            os.path.join(json_path, data['exp'] + '.json'), data_path)
        r=exp.edit_data(data,order)
        exp.save_json()
        messages = [('success',f'<{r}> note was saved.')]
    except Exception as e:
        messages = [('danger',f"Save data failed: {e}")]

    return jsonify(html=render_template('flash_messages.html', messages=messages), )

@app.route('/get_animal_data_figure/<path:filename>', methods=['GET'])
def get_animal_data_figure(filename):
    data_path = config['ANIMAL_DATA_PATH']
    return send_from_directory(data_path, filename, as_attachment=False)


if __name__ == "__main__":
    app.run()
