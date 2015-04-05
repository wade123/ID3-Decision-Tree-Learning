import math
class TreeNode:
    #the TreeNode definition for the output decision tree
    def __init__(self, attr = None):
        self.label = attr
        self.child = []

class DecisionTreeLearning:
    #the process of the ID3 algorithm
    def __init__(self, examples):
        self.examples = examples
        
    def get_attr_values(self, examples, attr):
        #get all possible values of a certain attribute
        res = []
        for instance in examples:
            res.append(instance[attr])
        return list(set(res))
        
    def selected_instances(self, examples, attr, attr_val):
        #get all instances that an attribute is a certain value
        res = []
        for instance in examples:
            if instance[attr] == attr_val:
                res.append(instance)
        return res
        
    def ID3(self, examples, target_attr, attrs):
        # the main process of ID3
        root = TreeNode()
        pos_examples = self.selected_instances(examples, target_attr, True)
        if len(examples) == len(pos_examples):
            root.label = 'Yes'
            return root
        if len(pos_examples) == 0:
            root.label = 'No'
            return root
        if len(attrs) == 0:
            root.label = 'Yes' if 2 * len(pos_examples) >= len(examples) else 'No'
            return root
        A = self.best_attr(examples, target_attr, attrs)
        root.label = A
        A_values = self.get_attr_values(self.examples, A)
        for A_val in A_values:
            examples_A_val = self.selected_instances(examples, A, A_val)
            if len(examples_A_val) == 0:
                node = TreeNode()
                node.label = 'Yes' if 2 * len(pos_examples) >= len(examples) else 'No'
            else:
                copy_attrs = attrs[:]
                copy_attrs.remove(A)
                node = self.ID3(examples_A_val, target_attr, copy_attrs)
            root.child.append([A_val, node])
        return root

    def best_attr(self, examples, target_attr, attrs):
        #pick the best classification attribute at one node
        res = []
        for attr in attrs:
            res.append(self.gain(examples, attr))
        return attrs[res.index(max(res))]
           
    def entropy(self, examples):
        #caculate the entropy of some instances 
        pos_examples = self.selected_instances(examples, target_attr,True)
        if len(pos_examples) == len(examples) or len(pos_examples) == 0:
            return 0
        else:
            pos = float(len(pos_examples)) / len(examples)
            return -1 * pos * math.log(pos,2) - (1 - pos) * math.log((1 - pos), 2)

    def gain(self, examples, attr):
        #calculate the information gain of a certain attribute for some instances
        res = self.entropy(examples)
        attr_vals = self.get_attr_values(self.examples, attr)
        for attr_val in attr_vals:
            examples_attr_val = self.selected_instances(examples, attr, attr_val)
            res -= (float(len(examples_attr_val))/len(examples)) * self.entropy(examples_attr_val)
        return res

#the training set for ID3
examples = [
{'Age': '2 years old', 'Sex': 'Male',   'Breed':'Pomeranian',          'Decision': False },
{'Age': '1 years old', 'Sex': 'Male',   'Breed':'Chihuahua',           'Decision': True},
{'Age': '4 years old', 'Sex': 'Female', 'Breed':'Australian Shepherd', 'Decision': True},
{'Age': '2 years old', 'Sex': 'Male',   'Breed':'Pit Bull',            'Decision': False},
{'Age': '1 years old', 'Sex': 'Male',   'Breed':'Australian Shepherd', 'Decision': True},
{'Age': '1 years old', 'Sex': 'Male',   'Breed':'Pit Bull',            'Decision': False},
{'Age': '1 years old', 'Sex': 'Female', 'Breed':'Australian Shepherd', 'Decision': False},
{'Age': '1 years old', 'Sex': 'Female', 'Breed':'Chihuahua',           'Decision': True},
{'Age': '4 years old', 'Sex': 'Female', 'Breed':'Pomeranian',          'Decision': False},
{'Age': '2 years old', 'Sex': 'Male',   'Breed':'Chihuahua',           'Decision': True},
{'Age': '2 years old', 'Sex': 'Female', 'Breed':'Pomeranian',          'Decision': True},
{'Age': '2 years old', 'Sex': 'Female', 'Breed':'Australian Shepherd', 'Decision': False},
] 
target_attr = 'Decision'
attrs = ['Age', 'Sex', 'Breed']
#test part
test = DecisionTreeLearning(examples)
node = test.ID3(examples, target_attr, attrs)

class Print:
    #functions used to generate the dot file used in Graphviz to show the output tree
    def __init__(self, num):
        self.num = num

    def p(self, node):
        if len(node.child) != 0:
            print 'attr' + str(self.num) + ' [shape="rectangle", label="' + node.label + '"]'
            num_copy = self.num
            for node_pair in node.child:
                self.num += 1
                if len(node_pair[1].child) == 0:                      
                    print 'attr' + str(num_copy) + ' -> ' + 'leaf' + str(self.num) + ' [label="' + node_pair[0] + '"]'                   
                else:
                    print 'attr' + str(num_copy) + ' -> ' + 'attr' + str(self.num) +' [label="' + node_pair[0] + '"]'
                self.p(node_pair[1])
        else:
            print 'leaf' + str(self.num) + ' [shape="plaintext", label="' + node.label + '"]'
        
print 'digraph G {' 
myPrint = Print(1)
myPrint.p(node)
print '}'
