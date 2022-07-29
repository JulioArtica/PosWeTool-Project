
import rospy
# Import the ROS message class under a different name
# to avoid confusion. We need it for the node state names.
from ros_bt_py_msgs.msg import Node as NodeMsg
# We need these to define a Node.
from ros_bt_py.node import Node, define_bt_node
from ros_bt_py.node_config import NodeConfig, OptionRef
@define_bt_node(NodeConfig(
    options={},
    inputs={},
    outputs={},
    max_children=None))
class MyAwesomeNode(Node):
    """This Node makes everything so much easier!"""
    def _do_setup(self):
        pass
    def _do_tick(self):
        return NodeMsg.FAILED
    def _do_shutdown(self):
        pass
    def _do_reset(self):
        return NodeMsg.IDLE
    def _do_untick(self):
        return NodeMsg.IDLE
    # Uncomment this if your node provides a utility calculation
    #
    # def _do_calculate_utility(self):
    # pass


######   Pushbutton block   #######
@define_bt_node(NodeConfig(
    version='0.9.0',
    options={'compare_type': type},
    inputs={
        'Input': OptionRef('compare_type'),
    },
    outputs={
        'act': int
        #'Output': OptionRef('compare_type')
    },
    max_children=0))
class DI_State(Leaf):
    
    def _do_setup(self):
        global mc
        port = rospy.get_param("~port", "/dev/ttyUSB0")
        baud = rospy.get_param("~baud", 115200)
        mc = MyCobot(port, baud)
        self.outputs['act'] = 0
        return NodeMsg.IDLE
 
    def _do_tick(self):

        #time.sleep(2)
        #mc.send_radians([0,0,0,0,0.1,0.2], 80)
        value = int(mc.get_basic_input(self.inputs['Input']))
        #pymycobot.__file__
        #wait for 2 seconds
        #time.sleep(2)
        if value == 1:
            self.outputs['act'] = 1
            return NodeMsg.SUCCEEDED
            #return NodeMsg.RUNNING
            #self.outputs['Output'] = value
        return NodeMsg.FAILED
        #return NodeMsg.RUNNING

    def _do_untick(self):
        # Nothing to do
        return NodeMsg.IDLE
 
    def _do_reset(self):
        # Reset output to False, so we'll return False until we
        # receive a new input.
        self.inputs.reset_updated()
 	
        return NodeMsg.IDLE
 
    def _do_shutdown(self):
        # Nothing to do
        pass


#######   Constant_v1 Position Cobot   #######
@define_bt_node(NodeConfig(
    version='0.9.0',
    options={
                'constant_type': type,
                'Joint1': OptionRef('constant_type'),
                'Joint2': OptionRef('constant_type'),
                'Joint3': OptionRef('constant_type'),
                'Joint4': OptionRef('constant_type'),
                'Joint5': OptionRef('constant_type'),
                'Joint6': OptionRef('constant_type'),
                'Velocity': int
            },
    inputs={},
    outputs={
                'J1': OptionRef('constant_type'),
                'J2': OptionRef('constant_type'),
                'J3': OptionRef('constant_type'),
                'J4': OptionRef('constant_type'),
                'J5': OptionRef('constant_type'),
                'J6': OptionRef('constant_type'),
                'Vel': int
            },
    max_children=0
        )
    )
class Constant_Joints(Leaf):

    def _do_setup(self):
        pass

    def _do_tick(self):
        self.outputs['J1'] = self.options['Joint1']
        self.outputs['J2'] = self.options['Joint2']
        self.outputs['J3'] = self.options['Joint3']
        self.outputs['J4'] = self.options['Joint4']
        self.outputs['J5'] = self.options['Joint5']
        self.outputs['J6'] = self.options['Joint6']
        self.outputs['Vel'] = self.options['Velocity']                
        return NodeMsg.SUCCEEDED

    def _do_shutdown(self):
        pass

    def _do_reset(self):
        return NodeMsg.IDLE

    def _do_untick(self):
        return NodeMsg.IDLE


#######  Set Angular Position Cobot   #######


@define_bt_node(NodeConfig(
    version='0.9.0',
    options={},
    inputs={
        'J1': float,
        'J2': float,
        'J3': float,
        'J4': float,
        'J5': float,
        'J6': float,
        'vel': int
    },
    outputs={},
    max_children=0)
)
class Robot_v1(Leaf):
    
    def _do_setup(self):
        global mc
        port = rospy.get_param("~port", "/dev/ttyUSB0")
        baud = rospy.get_param("~baud", 115200)
        mc = MyCobot(port, baud)
        return NodeMsg.IDLE
 
    def _do_tick(self):

        #self.outputs['formatted_string'] = str(mc)  #Vacio
        positions= [self.inputs['J1'],self.inputs['J2'],self.inputs['J3'],self.inputs['J4'],self.inputs['J5'],self.inputs['J6'],]
        mc.send_angles(positions, self.inputs['vel'])	
        return NodeMsg.SUCCEEDED


        # if self.inputs.is_updated('a') or self.inputs.is_updated('b'):
        #     if self.inputs['a'] == self.inputs['b']:
        #         return NodeMsg.SUCCEEDED
        #     else:
        #         return NodeMsg.FAILED
        # return NodeMsg.RUNNING

    def _do_untick(self):
        # Nothing to do
        return NodeMsg.IDLE
 
    def _do_reset(self):
        # Reset output to False, so we'll return False until we
        # receive a new input.
        self.inputs.reset_updated()
 	
        return NodeMsg.IDLE
 
    def _do_shutdown(self):
        # Nothing to do
        pass


#######   Take photo + send request VQC   #######


@define_bt_node(NodeConfig(
    version='0.9.0',
    options={'compare_type': type},
    inputs={
    },
    outputs={},
    max_children=0))
class Picture_VQC(Leaf):
    
    def _do_setup(self):

        return NodeMsg.IDLE
 
    def _do_tick(self):
        
        
        cap = cv2.VideoCapture(0)
        codec = cv2.VideoWriter_fourcc(	'M', 'J', 'P', 'G'	)
        cap.set(6, codec)
        cap.set(5, 30)
        cap.set(3, 1920)
        cap.set(4, 1080)
        ret, frame = cap.read()
        

        a = cv2.imwrite('/home/julio/smasp/shop4cf-bos-pilot/App/imgs/control/pieza.png',frame)
        time.sleep(2)
        #cap.release()
        #cv2.destroyAllWindows()
        
        url = "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:Device:Bosch:camera1/attrs"
        header = {"Content-Type": "application/json"}
        data = """{
                "pcb_path":{
                    "value":"/imgs/control/pieza.png",
                    "type":"Property"
                },
                "value":{
                    "type": "Property",
                    "value": "/imgs/template/template.png"
                }
            }"""

        resp1 = requests.patch(url, data, headers=header)
        time.sleep(3)
        os.system('cp /home/julio/smasp/shop4cf-bos-pilot/App/imgs/outcome/pieza_inspected.png /home/julio/smasp/ar-cvi/images/control_inspected.png') 
        time.sleep(3)
        url_2 = "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:Task:Megacal:task00012/attrs"
        data_2 = """{
            "workParameters": {
                "type": "Property",
                "value": {
                  "type":"Add",
                  "displayStatus":"inProgress",
                  "images":[

                      {   
                          "position":["0.17","0.025","0.0"],
                          "width":"500.0",
                          "height":"890.0",
                          "path":"/images/control_inspected.png"}
                  ]
                }
            },
            "@context": [
            ]
        }"""

        resp2 = requests.patch(url_2, data_2, headers=header)
        return NodeMsg.SUCCEEDED


    def _do_untick(self):
        # Nothing to do
        return NodeMsg.IDLE
 
    def _do_reset(self):
        # Reset output to False, so we'll return False until we
        # receive a new input.
        self.inputs.reset_updated()
 	
        return NodeMsg.IDLE
 
    def _do_shutdown(self):
        # Nothing to do
        pass





######    Wait   #######


@define_bt_node(NodeConfig(
    options={},
    inputs={
        'Time': int
    },
    outputs={},
    max_children=0))
class Wait(Leaf):
    
    def _do_setup(self):
        return NodeMsg.IDLE
 
    def _do_tick(self):
        time.sleep(self.inputs['Time'])	
        return NodeMsg.SUCCEEDED

    def _do_untick(self):
        # Nothing to do
        return NodeMsg.IDLE
 
    def _do_reset(self):
        # Reset output to False, so we'll return False until we
        # receive a new input.
        self.inputs.reset_updated()
 	
        return NodeMsg.IDLE
 
    def _do_shutdown(self):
        # Nothing to do
        pass





#######    Updating photo_VQC to ARCVI   #######


@define_bt_node(NodeConfig(
    version='0.9.0',
    options={'compare_type': type},
    inputs={
    },
    outputs={},
    max_children=0))
class Image_ARCVI(Leaf):
    
    def _do_setup(self):

        return NodeMsg.IDLE
 
    def _do_tick(self):
        
        url = "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:Task:Megacal:task00012/attrs"
        header = {"Content-Type": "application/ld+json"}
        data = """{
            "workParameters": {
                "type": "Property",
                "value": {
                  "type":"Add",
                  "displayStatus":"inProgress",
                  "images":[
                      {   
                          "position":["0.17","0.0","0.0"],
                          "width":"500.0",
                          "height":"890.0",
                          "path":"/images/Updating.png"}
                  ]
                }
            },
            "@context": [
            ]
        }"""

        resp = requests.patch(url, data, headers=header)

        return NodeMsg.SUCCEEDED


    def _do_untick(self):
        # Nothing to do
        return NodeMsg.IDLE
 
    def _do_reset(self):
        # Reset output to False, so we'll return False until we
        # receive a new input.
        self.inputs.reset_updated()
 	
        return NodeMsg.IDLE
 
    def _do_shutdown(self):
        # Nothing to do
        pass
