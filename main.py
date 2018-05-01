from flask import Flask, request, redirect, render_template
import cgi
import random

app = Flask(__name__)
app.config['DEBUG'] = True  

canvas_list = []
shapes_list = []
test = []
error = []
solved = []
paths = []
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.occupant = None
        self.color = None
    def __repr__(self):
        return str(self.x) + "," + str(self.y)

class Canvas():
    def __init__(self, width, height, points, area, shape_count):
        self.width = int(width)
        self.height = int(height)
        self.points = points
        self.mass = len(points)
        self.area = area
        self.shape_count = shape_count
        #
        x = []
        y = []
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
        #
        self.x=x
        self.y=y

    def __repr__(self):
        return str(self.points)

class Shape():
    def __init__(self, width, height, points, area, number, permutation):
        self.width = int(width)
        self.height = int(height)
        self.points = points
        self.mass = len(points)
        self.area = area
        self.number = number
        self.permutation = permutation
        self.location = []
        self.permutations = self.permutations()
        self.color = make_colors()
        for point in self.points:
            point.occupant = None
            self.location.append(None)
         #
        x = []
        y = []
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
        #
        self.x=x
        self.y=y

    def __repr__(self):
        return str(self.points)

    def clear(self):
        for i in range(len(self.points)):
            self.location[i] = None
            self.points[i].color = None

    def permutations(self):
        if self.permutation == 1:
            permutations = []
            x_y = self.points
            x_negative = []
            y_negative = []
            x_y_negative = []
            x_y_inverse = []
            x_negative_inverse = []
            y_negative_inverse = []
            x_y_negative_inverse = []

            shape_1 = self

            for point in self.points:
                #x_negative
                new_x = (point.x * -1) + (self.width - 1)
                new_y = point.y
                new_point = Point(new_x, new_y)
                x_negative.append(new_point)
                shape_2 = Shape(self.width, self.height, sorter(x_negative), self.area, self.number, 2)
                #y_negative
                new_x = point.x
                new_y = (point.y * -1) + (self.height - 1)
                new_point = Point(new_x, new_y)
                y_negative.append(new_point)
                shape_3 = Shape(self.width, self.height, sorter(y_negative), self.area, self.number, 3)
                #x_y_negative
                new_x = (point.x * -1) + (self.width - 1)
                new_y = (point.y * -1) + (self.height - 1)
                new_point = Point(new_x, new_y)
                x_y_negative.append(new_point)
                shape_4 = Shape(self.width, self.height, sorter(x_y_negative), self.area, self.number, 4)
                #x_y_inverse
            for point in shape_1.points:
                new_x = point.y
                new_y = point.x
                new_point = Point(new_x, new_y)
                x_y_inverse.append(new_point)
                shape_5 = Shape(self.height, self.width, sorter(x_y_inverse), self.area, self.number, 5)
                #x_negative_inverse
            for point in shape_2.points:
                new_x = point.y
                new_y = point.x
                new_point = Point(new_x, new_y)
                x_negative_inverse.append(new_point)
                shape_6 = Shape(self.height, self.width, sorter(x_negative_inverse), self.area, self.number, 6)
                #y_negative_inverse
            for point in shape_3.points:
                new_x = point.y 
                new_y = point.x
                new_point = Point(new_x, new_y)
                y_negative_inverse.append(new_point)
                shape_7 = Shape(self.height, self.width, sorter(y_negative_inverse), self.area, self.number, 7)
                #x_y_negative_inverse
            for point in shape_4.points:
                new_x = point.y
                new_y = point.x
                new_point = Point(new_x, new_y)
                x_y_negative_inverse.append(new_point)
                shape_8 = Shape(self.height, self.width, sorter(x_y_negative_inverse), self.area, self.number, 8)

            permutations.append(shape_1)
            permutations.append(shape_2)
            permutations.append(shape_3)
            permutations.append(shape_4)
            permutations.append(shape_5)
            permutations.append(shape_6)
            permutations.append(shape_7)
            permutations.append(shape_8)
            return trimmer(permutations)
        else:
            return None

def trimmer(permutations):
    #find repeats
        counter = 0 
        new_p=[]
        removes=[]
        for i in range(0, len(permutations)):
            for j in range (0, len(permutations)):
                if i == j:
                    break
                counter = 0
                for k in permutations[i].points:
                    for l in permutations[j].points:
                        match = False
                        if str(k) == str(l):
                            match = True
                            break
                    if match == True:
                        counter = counter + 1
                if counter == len(permutations[i].points) :
                    #message = permutations[i], "matches", permutations[j], "<br>"
                    #test.append(message)
                    removes.append(permutations[i].permutation)
                    break
                else:
                    #message = permutations[i], "doesn't match", permutations[j], "<br>"
                    #test.append(message)
                    pass
        for permutation in permutations:
            if permutation.permutation not in removes:
                new_p.append(permutation)
        for i in range(0, len(new_p)):
            new_p[i].permutation = i + 1
        return new_p

@app.route('/', methods=['GET', 'POST'])
def main():
    canvas_list.clear()
    shapes_list.clear()
    paths.clear()
    test.clear()
    error.clear()
    height = request.args.get('height')
    width = request.args.get('width')
    shape_count = request.args.get('shape_count')
    if height and width:    
        return render_template('canvas_shaper.html', height=int(height), width=int(width), shape_count = int(shape_count))
    return render_template('canvas_dimensions.html')

@app.route('/canvas', methods=['GET', 'POST'])
def canvas():
    height = request.args.get('height')
    width = request.args.get('width')
    shape_count =  request.args.get('shape_count')
    area = int(height) * int(width)
    canvas_points = []
    for i in range(0, int(height)):
        for j in range( 0, int(width)):
            on = request.args.get(str(j)+ "-" + str(i))
            if on == "on":
                point = Point(j, i)
                canvas_points.append(point)
    canvas = Canvas(width, height, canvas_points, area, shape_count)
    canvas_list.append(canvas)
    return render_template('shape_dimensions.html', canvas=canvas, counter=1, shape_count=shape_count)

@app.route('/shape_dimensions', methods=['GET', 'POST'])
def shape_dimensions():
    height = request.args.get('height')
    width = request.args.get('width')
    counter = request.args.get('counter')
    shape_count = request.args.get('shape_count')
    if height and width:    
        return render_template('shape_shaper.html', height=int(height), width=int(width), counter=counter, shape_count=shape_count)
    return render_template('shape_dimensions.html')

@app.route('/shape_shaper', methods=['GET', 'POST'])
def shape_shaper():
    height = request.args.get('height')
    width = request.args.get('width')
    counter = request.args.get('counter')
    shape_count = request.args.get('shape_count')
    area = int(height) * int(width)
    shape_points = []
    for i in range(0, int(height)):
        for j in range( 0, int(width)):
            on = request.args.get(str(j)+ "-" + str(i))
            if on == "on":
                point = Point(j, i)
                shape_points.append(point)
    shape=Shape(width, height, shape_points, area, counter, 1)
    shapes_list.append(shape)
    if shape_count == counter:
        return redirect('/solve')
    else:
        return render_template('shape_dimensions.html', canvas=canvas, counter=(int(counter)+1), shape_count=shape_count)

@app.route('/solve', methods=['GET', 'POST'])
def solve():
    shape_sorter(shapes_list)
    colors = []
    for shape in shapes_list:
        colors.append(shape.color)
    return render_template('solve.html', canvas=canvas, canvas_output=canvas_output(), shapes_output=shape_output(), colors=colors)

@app.route('/solver', methods=['GET', 'POST'])
def solver():
    colors = []
    for shape in shapes_list:
        colors.append(shape.color)
    test.append("<hr>")
    canvas = canvas_list[0]
    path = []
    for canvas_point in canvas.points:
        shape_path = []
        fit = False
        if canvas_point.occupant == None:
            for shape in shapes_list:
                shape_path = []
                fit = False
                if shape.location[0] == None:
                    save_permutation = None
                    for permutation in shape.permutations:
                        #return str(canvas_fit(canvas, permutation, canvas_point))
                        if canvas_fit(canvas, permutation, canvas_point, shape.color) == False:
                            message = "|" + str(shape.number) + "." + str(permutation.permutation) + "|" + " - MISS - |" + str(canvas_point) + "|<br>"
                            test.append(message)
                            shape.clear()
                            for point in canvas.points:
                                if point.occupant == shape.number:
                                    point.occupant = None
                                    point.color = None
                        else:
                            message = "|" + str(shape.number) + "." + str(permutation.permutation) + "|" + " - HIT - |" + str(canvas_point) + "|<br>"
                            test.append(message)
                            fit = True
                        if fit == True:
                            save_permutation = permutation
                            for i in range(0, len(shape.points)):
                                x = shape.points[i].x + (canvas_point.x - shape.points[0].x)
                                y = shape.points[i].y + (canvas_point.y - shape.points[0].y)
                                shape.location[i] = Point(x, y)
                            break
                    if fit == True:
                        shape_path.append(shape.number)
                        shape_path.append(save_permutation.permutation) 
                        shape_path.append(save_permutation.location[0])
                        break
                else: 
                    pass
        if len(shape_path) != 0:
            paths.append(shape_path)
    counter = 0
    test.append("<hr>")
    for canvas_point in canvas.points:
        if canvas_point.occupant != None:
            message = str(canvas_point.occupant)
        else:
            message = str("0")
        test.append(message)
        counter = counter + 1
        if counter == canvas.width:
            test.append("<br>")
            counter = 0
    test.append("<hr>")
    for shape in shapes_list:
        message = str(shape) + "-" + str(shape.number) + "<br>"
        test.append(message)
        message = str(shape.location) + "-" + str(shape.number) + "<br>"
        test.append(message)

    #return str(test) + str(error)
    owned = True
    for point in canvas.points:
        if point.occupant == None:
            owned = False
    if owned == True:
        return render_template('solve.html', canvas=canvas, canvas_output=canvas_output(), shapes_output=shape_output(), colors=colors, solution_output=solution_output(), paths=paths)
    else:
        return render_template('solve.html', canvas=canvas, canvas_output=canvas_output(), shapes_output=shape_output(), colors=colors, solution_output=solution_output(), paths=paths, test=test, error=error)
        #return str(test) + str(error) + str(paths)
def canvas_fit(canvas, shape, origin, color): #returns a True or False
    count = 0
    for i in range(0, len(shape.points)):
        x = shape.points[i].x + (origin.x - shape.points[0].x)
        y = shape.points[i].y + (origin.y - shape.points[0].y)
        shape.location[i] = Point(x, y)
    for i in range(0, len(shape.location)):
        fit = False
        origin_found = False
        for canvas_point in canvas.points:
            if str(canvas_point) != str(origin):
                pass
            else:
                origin_found = True
            if origin_found == True: 
                if str(shape.location[i]) == str(canvas_point) and canvas_point.occupant == None:
                    canvas_point.occupant = shape.number
                    canvas_point.color = color
                    count = count + 1
                    test.append("x")
                    error.append(str(shape.location))
                    message = str(shape.location[i]) + "---" + str(canvas_point) + "---" +str(shape.number) + "." + str(shape.permutation) + "PASS<br>" 
                    error.append(message)
                else:
                    message = str(shape.location[i]) + "---" + str(canvas_point) + "---" +str(shape.number) + "." + str(shape.permutation) + "FAIL<br>"
                    error.append(message)
    if count == shape.mass:
        return True
    else:
        return False

def sorter(points):
    check = False
    for i in range(0, len(points)-1): 
        if points[i].y > points[i+1].y:
            placeholder = points[i]
            points[i] = points[i+1]
            points[i+1] = placeholder
            check = True
        elif points[i].y == points[i+1].y:
            if points[i].x > points[i+1].x:
                placeholder = points[i]
                points[i] = points[i+1]
                points[i+1] = placeholder
                check = True
        else:
            pass
    if check == True:
        sorter(points)
    
    return points

def shape_sorter(shapes):
    check = False
    for i in range(0, len(shapes)-1): 
        if shapes[i].mass < shapes[i+1].mass:
            placeholder = shapes[i]
            shapes[i] = shapes[i+1]
            shapes[i+1] = placeholder
            check = True
        elif shapes[i].mass == shapes[i+1].mass:
            if len(shapes[i].permutations) > len(shapes[i+1].permutations):
                placeholder = shapes[i]
                shapes[i] = shapes[i+1]
                shapes[i+1] = placeholder
                check = True
        else:
            pass

    if check == True:
        shape_sorter(shapes)

    for i in range(0, len(shapes)):
        shapes[i].number = i + 1



def make_colors():
    pallete = [str(random.choice(range(256))), str(random.choice(range(256))), str(random.choice(range(256)))]
    color = "rgb(" + pallete[0] + ", " + pallete[1] + ", " + pallete[2] + ")"
    return color

def shape_output():
    permutation_output = []
    shape_output = []
    shapes_output = []

    for shape in shapes_list:
        shape_output = []
        colors = []
        colors.append(shape.color)
        for permutation in shape.permutations:
            permutation_output = []
            for i in range (0, permutation.height):
                row = []
                for j in range (0, permutation.width):
                    for point in permutation.points:
                        if point.x == j and point.y == i:
                            check = True
                            break
                        else: 
                            check = False
                    if check == True:
                        row.append(True)
                    else:
                        row.append(False)
                permutation_output.append(row)
            shape_output.append(permutation_output)
        shapes_output.append(shape_output)   
    return shapes_output

def canvas_output():
    canvas=canvas_list[0]
    canvas_output = []
    for i in range (0, canvas.height):
        row = []
        for j in range (0, canvas.width):
            for point in canvas.points:
                if point.x == j and point.y == i:
                    check = True
                    break
                else: 
                    check = False
            if check == True:
                row.append(True)
            else:
                row.append(False)
        canvas_output.append(row)
    return canvas_output
def solution_output():
    canvas=canvas_list[0]
    solution_output = []
    for i in range (0, canvas.height):
        row = []
        for j in range (0, canvas.width):
            for point in canvas.points:
                if point.x == j and point.y == i:
                    check = True
                    break
                else: 
                    check = False
            if check == True:
                row.append(point.color)
            else:
                row.append(None)
        solution_output.append(row)
    return solution_output

if __name__ == "__main__":
    app.run()

