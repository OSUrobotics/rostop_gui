#!/usr/bin/env python
# when using rosbuild these lines are required to make sure that all dependent Python packages are on the PYTHONPATH:
import roslib
roslib.load_manifest('rostop')


import os
import rospy

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtGui import QTableWidget, QTableWidgetItem, QPushButton
from python_qt_binding.QtCore import Qt, QTimer

from rostop.node_info import NodeInfo
from functools import partial


class RosTop(Plugin):

    node_fields   = [        'pid', 'get_cpu_percent', 'get_memory_percent', 'get_num_threads']
    out_fields    = [        'pid', 'cpu_percent',     'memory_percent',     'num_threads'    ]
    format_fields = [         '%s', '%0.2f%%',         '%0.2f%%',            '%s'             ]
    node_labels   = ['Node', 'PID', 'CPU %',           'Mem %',              'Num Threads'    ]

    _node_info = NodeInfo()

    def __init__(self, context):
        super(RosTop, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('RosTop')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                      dest="quiet",
                      help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns

        # Create QWidget
        self._table_widget = QTableWidget()
        self._table_widget.setObjectName('TopTable')
        context.add_widget(self._table_widget)
        self._table_widget.setColumnCount(len(self.node_labels))
        self._table_widget.setHorizontalHeaderLabels(self.node_labels)
        self._table_widget.setSortingEnabled(True)
        self.update_table()
        self.update_table()
        self._update_timer = QTimer()
        self._update_timer.setInterval(1000)
        self._update_timer.timeout.connect(self.update_table)
        self._update_timer.start()

    def update_one_item(self, nx, node_name, process):
        self._table_widget.setItem(nx, 0, QTableWidgetItem(node_name))
        info = process.as_dict(self.node_fields)
        # info['cpu_percent'] = process.get_cpu_percent()
        for fx, field in enumerate(self.out_fields):
            val = info[field]
            twi = QTableWidgetItem()
            twi.setData(Qt.EditRole, val)
            self._table_widget.setItem(nx, fx+1, twi)

    def update_table(self):
        self._table_widget.clearContents()
        infos = self._node_info.get_all_node_info()
        self._table_widget.setRowCount(len(infos))
        for nx, (node_name, process) in enumerate(infos):
            self.update_one_item(nx, node_name, process)
            # QTimer.singleShot(0, updateme)        

    def shutdown_plugin(self):
        self._update_timer.stop()

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    #def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure it
        # Usually used to open a configuration dialog
