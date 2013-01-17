#!/usr/bin/env python
# when using rosbuild these lines are required to make sure that all dependent Python packages are on the PYTHONPATH:
import roslib
roslib.load_manifest('rostop')


import os
import rospy

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtGui import QLabel, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QCheckBox, QWidget, QToolBar, QLineEdit
from python_qt_binding.QtCore import Qt, QTimer

from rostop.node_info import NodeInfo
from functools import partial
from pprint import pprint

class RosTop(Plugin):

    node_fields   = [             'pid', 'get_cpu_percent', 'get_memory_percent', 'get_num_threads']
    out_fields    = ['node_name', 'pid', 'cpu_percent',     'memory_percent',     'num_threads'    ]
    format_fields = [             '%s',  '%0.2f%%',         '%0.2f%%',            '%s'             ]
    node_labels   = ['Node',      'PID', 'CPU %',           'Mem %',              'Num Threads'    ]

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

        # Setup the toolbar
        self._toolbar = QToolBar()
        # context.add_toolbar(self._toolbar)
        self._filter_box = QLineEdit()
        self._regex_box  = QCheckBox()
        self._regex_box.setText('regex')
        self._toolbar.addWidget(QLabel('Filter'))
        self._toolbar.addWidget(self._filter_box)
        self._toolbar.addWidget(self._regex_box)


        # self.button.clicked.connect(lambda : self.update_table())

        self._container = QWidget()
        self._layout    = QVBoxLayout()
        self._container.setLayout(self._layout)

        # Create QWidget
        self._table_widget = QTableWidget()
        self._table_widget.setObjectName('TopTable')
        self._table_widget.setColumnCount(len(self.node_labels))
        self._table_widget.setHorizontalHeaderLabels(self.node_labels)
        self._table_widget.setSortingEnabled(True)


        self._layout.addWidget(self._table_widget)
        # context.add_widget(self._layout)
        context.add_widget(self._container)

        # self._table_widget.horizontalHeader().sortIndicatorChanged.connect(self._sortIndicatorChanged)

        self.update_table()
        self.update_table()
        self._update_timer = QTimer()
        self._update_timer.setInterval(1000)
        self._update_timer.timeout.connect(self.update_table)
        self._update_timer.start()

    def _sortIndicatorChanged(self, logicalIndex, order):
        print logicalIndex, order
        print self._table_widget.horizontalHeader().sortIndicatorSection(),
        print self._table_widget.horizontalHeader().sortIndicatorOrder()
        print '===='

    def _filter_node(self, node_name):
        pass        

    def update_one_item(self, nx, info):
        # twi = QTableWidgetItem(info['node_name'])
        # twi.setFlags(twi.flags() ^ Qt.ItemIsEditable)
        # self._table_widget.setItem(nx, 0, twi)
        for fx, field in enumerate(self.out_fields):
            self._table_widget.removeCellWidget(nx, fx)
            val = info[field]
            twi = QTableWidgetItem()
            twi.setData(Qt.EditRole, val)
            twi.setFlags(twi.flags() ^ Qt.ItemIsEditable)
            self._table_widget.setItem(nx, fx, twi)

    def update_table(self):
        # self._table_widget.clearContents()
        infos = self._node_info.get_all_node_fields(self.node_fields)
        self._table_widget.setRowCount(len(infos))
        # asc = 0, desc = 1
        sort_section = self._table_widget.horizontalHeader().sortIndicatorSection()
        sort_order = self._table_widget.horizontalHeader().sortIndicatorOrder()

        if sort_section >= len(self.out_fields):
            sort_section = 0

        for nx, info in enumerate(sorted(infos, key=lambda x: x[self.out_fields[sort_section]], reverse=sort_order)):
            self.update_one_item(nx, info)

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
