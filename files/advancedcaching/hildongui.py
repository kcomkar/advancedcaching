#!/usr/bin/python
# -*- coding: utf-8 -*-

#        Copyright (C) 2009 Daniel Fett
#         This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#        Author: Daniel Fett advancedcaching@fragcom.de
#

 
# deps: python-html python-image python-netclient python-misc python-pygtk python-mime python-json

# todo:
# download logs
# parse attributes
# add "next waypoint" button
# add description to displayed images
# add translation support?
# download in seperate thread?


 
### For the gui :-)


import geo
import geocaching
import gtk
import openstreetmap
import os
import re
import hildon
from simplegui import SimpleGui
class HildonGui(SimpleGui):

    USES = ['locationgpsprovider']
    
    def __init__(self, core, pointprovider, userpointprovider, dataroot):
        gtk.gdk.threads_init()
        self.ts = openstreetmap.TileServer()
        openstreetmap.TileLoader.noimage = gtk.gdk.pixbuf_new_from_file(os.path.join(dataroot, 'noimage.png'))
                
        self.core = core
        self.pointprovider = pointprovider
        self.userpointprovider = userpointprovider
                
        self.format = geo.Coordinate.FORMAT_DM

        # @type self.current_cache geocaching.GeocacheCoordinate
        self.current_cache = None
                
        self.current_target = None
        self.gps_data = None
        self.gps_has_fix = False
        self.gps_last_position = None
        self.banner = None
                
        self.dragging = False
        self.block_changes = False
                
        self.pixmap_north_indicator = None
        self.drawing_area_configured = self.drawing_area_arrow_configured = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.notes_changed = False
        self.map_center_x, self.map_center_y = 100, 100
        self.inhibit_zoom = False
        self.inhibit_expose = False
        
        gtk.set_application_name("Geocaching Tool")
        program = hildon.Program.get_instance()
        self.window = hildon.StackableWindow()
        program.add_window(self.window)
        self.window.connect("delete_event", gtk.main_quit, None)
        self.window.add(self._create_main_view())
        self.window.set_app_menu(self._create_main_menu())

    def _create_main_view(self):
        root = gtk.VBox()

        self.main_gpspage = gtk.Table(6, 2)
        self.drawing_area_arrow = gtk.DrawingArea()

        '''
        self.label_dist = gtk.Label("Distance")
        self.label_bearing = gtk.Label("Bearing")
        self.label_altitude = gtk.Label("Altitude")
        self.label_latlon = gtk.Label("LatLon")
        self.label_target = gtk.Label("Target")
        self.label_quality = gtk.Label("Quality")
        '''

        self.label_dist = gtk.Label()
        self.label_dist.set_markup("Distance\n<small>312 km</small>")
        self.label_dist.set_alignment(0, 0)

        self.label_bearing = gtk.Label()
        self.label_bearing.set_markup("Bearing\n<small>123°</small>")
        self.label_bearing.set_alignment(0, 0)

        self.label_altitude = gtk.Label()
        self.label_altitude.set_markup("Altitude\n<small>123 m</small>")
        self.label_altitude.set_alignment(0, 0)

        self.label_latlon = gtk.Label()
        self.label_latlon.set_markup("Current Position\n<small>N49 54.121 E4 12.249</small>")
        self.label_latlon.set_alignment(0, 0)

        self.label_quality = gtk.Label()
        self.label_quality.set_markup("Accurancy\n<small>4/12 Sats, +- 12m</small>")
        self.label_quality.set_alignment(0, 0)

        button = hildon.Button(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        button.set_title("Target")
        button.set_value('N49 54.121 E4 12.249')
        button.connect('clicked', self._on_show_dialog_change_target, None)
        self.label_target = button


        '''
        gpsinfo = gtk.VBox()
        gpsinfo.pack_start(self.label_dist, True, False)
        gpsinfo.pack_start(self.label_bearing, True, False)
        gpsinfo.pack_start(self.label_altitude, True, False)
        gpsinfo.pack_start(self.label_latlon, True, False)
        gpsinfo.pack_start(self.label_quality, True, False)
        gpsinfo.pack_start(self.label_target, True, False)


        self.main_gpspage.pack_start(self.drawing_area_arrow, True, True)
        self.main_gpspage.pack_start(gpsinfo, False, True)
        '''


        self.main_gpspage.attach(self.drawing_area_arrow, 1, 2, 0, 6, gtk.EXPAND | gtk.FILL, gtk.EXPAND)
        self.main_gpspage.attach(self.label_dist, 0, 1, 0, 1, gtk.FILL, gtk.EXPAND)
        self.main_gpspage.attach(self.label_bearing, 0, 1, 1, 2, gtk.FILL, gtk.EXPAND)
        self.main_gpspage.attach(self.label_altitude, 0, 1, 2, 3, gtk.FILL, gtk.EXPAND)
        self.main_gpspage.attach(self.label_latlon, 0, 1, 3, 4, gtk.FILL, gtk.EXPAND)
        self.main_gpspage.attach(self.label_quality, 0, 1, 4, 5, gtk.FILL, gtk.EXPAND)
        self.main_gpspage.attach(self.label_target, 0, 1, 5, 6, gtk.FILL, gtk.EXPAND)

        self.main_mappage = gtk.VBox()
        self.drawing_area = gtk.DrawingArea()

        buttons = gtk.HBox()

        button = hildon.CheckButton(gtk.HILDON_SIZE_FINGER_HEIGHT)
        button.set_label("track")
        button.connect("clicked", self._on_track_toggled, None)
        self.button_track = button
        buttons.pack_start(button, True, True)

        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("Update Geocaches")
        button.connect("clicked", self.on_download_clicked, None)
        buttons.pack_start(button, True, True)

        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("+")
        button.connect("clicked", self._on_zoomin_clicked, None)
        buttons.pack_start(button, True, True)



        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("-")
        button.connect("clicked", self._on_zoomout_clicked, None)
        buttons.pack_start(button, True, True)
        self.main_mappage.pack_start(self.drawing_area, True)
        self.main_mappage.pack_start(buttons, False)
        root.pack_start(self.main_gpspage, True)
        root.pack_start(self.main_mappage, True)


        self.drawing_area.set_double_buffered(False)
        self.drawing_area.connect("expose_event", self._expose_event)
        self.drawing_area.connect("configure_event", self._configure_event)
        self.drawing_area.connect("button_press_event", self._drag_start)
        self.drawing_area.connect("scroll_event", self._scroll)
        self.drawing_area.connect("button_release_event", self._drag_end)
        self.drawing_area.connect("motion_notify_event", self._drag)
        self.drawing_area.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.SCROLL)

        # arrow drawing area
        self.drawing_area_arrow.connect("expose_event", self._expose_event_arrow)
        self.drawing_area_arrow.connect("configure_event", self._configure_event_arrow)
        self.drawing_area_arrow.set_events(gtk.gdk.EXPOSURE_MASK)
        return root
            
    def _create_main_menu(self):
        menu = hildon.AppMenu()
    
        button = hildon.Button(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        button.set_title("Go to Target")
        button.set_value('No target set')
        button.connect("clicked", self.on_show_target_clicked, None)
        menu.append(button)
        self.button_goto_target = button
        
        
        button = hildon.Button(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        button.set_title("Set Center as Target")
        button.set_value('N49 42.123 E6 21.402')
        button.connect("clicked", self._on_set_target_center, None)
        menu.append(button)
        self.button_center_as_target = button
        
        
        button = hildon.Button(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        button.set_title("Show Details for selected")
        button.set_value('Der Zerstreute Professor...')
        button.connect("clicked", self._on_show_cache_details, None)
        menu.append(button)
        self.button_show_details = button
        
    
        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("Search Geocaches")
        button.connect("clicked", self._on_show_search, None)
        menu.append(button)
    
        button = hildon.Button(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        button.set_title("Upload Fieldnote(s)")
        button.set_value("You have created 2 fielnotes.")
        button.connect("clicked", self._on_upload_fieldnotes, None)
        menu.append(button)
        
    
        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("Download Details")
        button.connect("clicked", self.on_download_details_map_clicked, None)
        menu.append(button)
    
    
        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("Options")
        button.connect("clicked", self._on_show_options, None)
        menu.append(button)
    
        button1 = hildon.GtkRadioButton(gtk.HILDON_SIZE_AUTO, None)
        button1.set_label("GPS")
        button1.set_mode(False)
        button1.connect("toggled", self._on_set_active_page, None)
        button2 = hildon.GtkRadioButton(gtk.HILDON_SIZE_AUTO, button1)
        button2.set_label("Map")
        button2.set_mode(False)
        self.button_toggle_view_gps = button1
        self.button_toggle_view_map = button2
        self.button_toggle_view_map.set_active(True)
        menu.add_filter(button1)
        menu.add_filter(button2)
        menu.show_all()
        return menu

    def _drag_end(self, widget, event):
        SimpleGui._drag_end(self, widget, event)
        c = self.ts.num2deg(self.map_center_x, self.map_center_y)
        self.button_center_as_target.set_value("%s %s" % (c.get_lat(self.format), c.get_lon(self.format)))


    def show(self):
        self.window.show_all()
        self._on_set_active_page()
        gtk.main()
        
        
    def _on_show_search(self, widget, data):
        
        dialog = gtk.Dialog("search for...", None, gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        
        sel_size = hildon.TouchSelector(text=True)
        sel_size.append_text('micro')
        sel_size.append_text('small')
        sel_size.append_text('regular')
        sel_size.append_text('huge')
        sel_size.append_text('other')
        sel_size.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)
        pick_size = hildon.PickerButton(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        pick_size.set_selector(sel_size)
        pick_size.set_title("Select Size(s)")
        for i in range(5):
            sel_size.select_iter(0, sel_size.get_model(0).get_iter(i), False)
        
        sel_type = hildon.TouchSelector(text=True)
        sel_type.append_text('traditional')
        sel_type.append_text('multi')
        sel_type.append_text('virtual')
        sel_type.append_text('earth')
        sel_type.append_text('all types')
        sel_type.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)
        pick_type = hildon.PickerButton(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        pick_type.set_selector(sel_type)
        pick_type.set_title("Select Type(s)")
        sel_type.unselect_all(0)
        sel_type.select_iter(0, sel_type.get_model(0).get_iter(4), False)
        
        sel_status = hildon.TouchSelector(text=True)
        sel_status.append_text('all')
        sel_status.append_text('not found')
        sel_status.append_text('found')
        sel_status.append_text('marked')
        sel_status.append_text('not found & marked')
        pick_status = hildon.PickerButton(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        pick_status.set_selector(sel_status)
        pick_status.set_title("Select Status")
        
        sel_status.unselect_all(0)
        sel_status.select_iter(0, sel_status.get_model(0).get_iter(0), False)
                        
        sel_diff = hildon.TouchSelector(text=True)
        sel_diff.append_text('1..2.5')
        sel_diff.append_text('3..4')
        sel_diff.append_text('4.5..5')
        sel_diff.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)
        pick_diff = hildon.PickerButton(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        pick_diff.set_selector(sel_diff)
        pick_diff.set_title("Select Difficulty")
        for i in range(3):
            sel_diff.select_iter(0, sel_diff.get_model(0).get_iter(i), False)
                        
        sel_terr = hildon.TouchSelector(text=True)
        sel_terr.append_text('1..2.5')
        sel_terr.append_text('3..4')
        sel_terr.append_text('4.5..5')
        sel_terr.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_MULTIPLE)
        pick_terr = hildon.PickerButton(gtk.HILDON_SIZE_AUTO, hildon.BUTTON_ARRANGEMENT_VERTICAL)
        pick_terr.set_selector(sel_terr)
        pick_terr.set_title("Select Terrain")
        for i in range(3):
            sel_terr.select_iter(0, sel_terr.get_model(0).get_iter(i), False)
        
        check_visible = gtk.CheckButton("in current map view")
        
        name = hildon.Entry(gtk.HILDON_SIZE_AUTO)
        name.set_placeholder("search for name...")
        
        t = gtk.Table(4, 2)
        t.attach(name, 0, 2, 0, 1)
        t.attach(pick_size, 0, 1, 1, 2)
        t.attach(pick_diff, 1, 2, 1, 2)
        t.attach(pick_type, 0, 1, 2, 3)
        t.attach(pick_terr, 1, 2, 2, 3)
        t.attach(check_visible, 0, 1, 3, 4)
        t.attach(pick_status, 1, 2, 3, 4)
        
        dialog.vbox.pack_start(t)
        
        dialog.show_all()
        dialog.run()
        dialog.hide()
        
           
        
        win = hildon.StackableWindow()
        win.set_title("Search results")
        
        ls = gtk.ListStore(str, str, str, object)
        ls.append(['Der zerstreute Professor vom Trimmelter Hof', 'micro', 'D2.5 T3', hildon.StackableWindow()])             
        tv = hildon.TouchSelector()
        col1 = tv.append_column(ls, gtk.CellRendererText())
        
        c1cr = gtk.CellRendererText()
        c2cr = gtk.CellRendererText()
        c3cr = gtk.CellRendererText()
        
        col1.pack_start(c1cr, True)
        col1.pack_end(c2cr, True)
        col1.pack_start(c3cr, True)

        col1.set_attributes(c1cr, text=0)
        col1.set_attributes(c2cr, text=1)
        col1.set_attributes(c3cr, text=2)
        
        def select_cache(widget, data, more):
            rows = tv.get_selected_rows(0)
            self._select_cache(ls[rows[0]][3])
        
        tv.connect("changed", select_cache, None)
        
        win.add(tv)
        win.show_all()
        
        
        
    def _on_show_options(self, widget, data):
        dialog = gtk.Dialog("options", None, gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        
        opts = gtk.Table(5, 2)
        opts.attach(gtk.Label("Username"), 0, 1, 0, 1)
        username = hildon.Entry(gtk.HILDON_SIZE_AUTO)
        opts.attach(username, 1, 2, 0, 1)
        
        opts.attach(gtk.Label("Password"), 0, 1, 1, 2)
        password = hildon.Entry(gtk.HILDON_SIZE_AUTO)
        password.set_visibility(False)
        opts.attach(password, 1, 2, 1, 2)
        
        check_dl_images = gtk.CheckButton("Don't Download Images")
        check_show_cache_id = gtk.CheckButton("Show Geocache ID on Map")
        check_hide_found = gtk.CheckButton("Hide Found Geocaches on Map")
        
        opts.attach(check_dl_images, 0, 2, 2, 3)
        opts.attach(check_show_cache_id, 0, 2, 3, 4)
        opts.attach(check_hide_found, 0, 2, 4, 5)
        
        dialog.vbox.pack_start(opts)
        
        
        dialog.show_all()
        result = dialog.run()
        dialog.hide()
                
    def _on_show_dialog_change_target(self, widget, data):
        dialog = gtk.Dialog("change target", None, gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        h_lat = gtk.HBox()        
        l_lat = gtk.Label("Latitude: ")
        e_lat = gtk.Entry()
        e_lat.set_text("N49 44.123")
        h_lat.pack_start(l_lat, True)
        h_lat.pack_start(e_lat, True)
        
        h_lon = gtk.HBox()        
        l_lon = gtk.Label("Longitude: ")
        e_lon = gtk.Entry()
        e_lon.set_text("E6 22.123")
        h_lon.pack_start(l_lon, True)
        h_lon.pack_start(e_lon, True)
        
        dialog.vbox.pack_start(h_lat)
        dialog.vbox.pack_start(h_lon)
        
        
        dialog.show_all()
        result = dialog.run()
        dialog.hide()
        if result == gtk.RESPONSE_ACCEPT:
            self.set_target(geo.try_parse_coordinate("%s %s" % (e_lat.get_text(), e_lon.get_text())))

    def set_active_page(self, map):
        self.button_toggle_view_gps.set_active(not map)
        self.button_toggle_view_map.set_active(map)
        self._on_set_active_page()
        
    def _on_set_active_page(self, widget = None, data = None):

        widget = self.button_toggle_view_gps
        a = widget.get_active()
        if a:
            self.main_gpspage.show()
            self.main_mappage.hide()
        else:
            self.main_gpspage.hide()
            self.main_mappage.show()
        
    def _on_tracked_toggled(self, widget, data):
        pass
        
    def _on_zoom_in(self, widget, data):
        pass
        
        
    def _on_zoom_out(self, widget, data):
        pass
        
        
        
        
    def _on_show_cache_details(self, widget, data, touched=None):
        self.show_cache(self.current_cache)
        pass

    def show_cache(self, cache):
        if cache == None:
            return
        self.current_cache = cache

        win = hildon.StackableWindow()
        win.set_title(cache.title)
        
        c = {}
    
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_BOTTOM)
        
        # info
        p = gtk.Table(9, 2)
        labels = (
                  ('Full Name', 'name', cache.title),
                  ('ID', 'id', cache.name),
                  ('Type', 'type', cache.type),
                  ('Size', 'size', cache.get_size_string()),
                  ('Terrain', 'terrain', cache.get_terrain()),
                  ('Difficulty', 'difficulty', cache.get_difficulty()),
                  ('Owner', 'owner', cache.owner),
                  ('Status', 'status', cache.get_status())
                  )
        i = 0
        for label, name, text in labels:
            l = gtk.Label()
            l.set_alignment(0, 0.5)
            l.set_markup("<b>%s</b>" % label)
            w = gtk.Label(text)
            w.set_line_wrap(True)
            w.set_alignment(0, 0.5)
            c[name] = w
            p.attach(l, 0, 1, i, i + 1)
            p.attach(w, 1, 2, i, i + 1)
            i += 1
        if not cache.was_downloaded():
            p.attach(gtk.Label("Please download full details to see the description."), 0, 2, 8, 9)
        
        notebook.append_page(p, gtk.Label("info"))

        if cache.was_downloaded():
        
            # desc
            p = hildon.PannableArea()
            vp = gtk.Viewport()
            p.add(vp)
            c['desc'] = gtk.Label()
            c['desc'].set_line_wrap(True)
            c['desc'].set_alignment(0, 0)
            c['desc'].set_size_request(self.window.size_request()[0] - 10, -1)
            vp.add(c['desc'])

            notebook.append_page(p, gtk.Label("description"))
            if cache.was_downloaded():
                text_shortdesc = self._strip_html(cache.shortdesc)
                if cache.status == geocaching.GeocacheCoordinate.STATUS_DISABLED:
                    text_shortdesc = 'This Cache is not available!\n' + text_shortdesc
                text_longdesc = self._strip_html(re.sub(r'(?i)<img[^>]+?>', ' [to get all images, re-download description] ', re.sub(r'\[\[img:([^\]]+)\]\]', lambda a: self._replace_image_callback(a, cache), cache.desc)))

                if text_longdesc == '':
                    text_longdesc = '(no Description available)'
                if not text_shortdesc == '':
                    showdesc = text_shortdesc + "\n\n" + text_longdesc
                else:
                    showdesc = text_longdesc
                c['desc'].set_text(showdesc)
            else:
                c['desc'].set_text("Please download full details to see the description.")



            # logs&hints
            p = hildon.PannableArea()
            vp = gtk.Viewport()
            p.add(vp)
            c['hints'] = gtk.Label()
            c['hints'].set_line_wrap(True)
            c['hints'].set_alignment(0, 0)
            c['hints'].set_size_request(self.window.size_request()[0] - 10, -1)
            vp.add(c['hints'])
            notebook.append_page(p, gtk.Label("hints & logs"))

            logs = cache.get_logs()
            if len(logs) > 0:
                text_hints = 'LOGS:\n'
                for l in logs:
                    if l['type'] == geocaching.GeocacheCoordinate.LOG_TYPE_FOUND:
                        t = 'FOUND'
                    elif l['type'] == geocaching.GeocacheCoordinate.LOG_TYPE_NOTFOUND:
                        t = 'NOT FOUND'
                    elif l['type'] == geocaching.GeocacheCoordinate.LOG_TYPE_NOTE:
                        t = 'NOTE'
                    elif l['type'] == geocaching.GeocacheCoordinate.LOG_TYPE_MAINTENANCE:
                        t = 'MAINTENANCE'
                    else:
                        t = l['type'].upper()
                    text_hints += '%s by %s at %4d/%d/%d: %s\n\n' % (t, l['finder'], int(l['year']), int(l['month']), int(l['day']), l['text'])
                text_hints += '\n----------------\n'
            else:
                text_hints = 'No Logs.\n\n'
            c['hints'].set_text(text_hints)

            # images
            p = gtk.Label("This is not implemented yet, sorry!")
            notebook.append_page(p, gtk.Label("images"))      
        
        # coords

        p = gtk.VBox()
        c['coords'] = hildon.TouchSelector(text=True)
        c['coords'].set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE)

        format = lambda n: "%s %s" % (re.sub(r' ', '', n.get_lat(self.format)), re.sub(r' ', '', n.get_lon(self.format)))
        c['coords'].append_text("First Waypoint: %s" % format(cache))
        for w in cache.get_waypoints():
            latlon = format(geo.Coordinate(w['lat'], w['lon'])) if not (w['lat'] == -1 and w['lon'] == -1) else "???"
            c['coords'].append_text("%s - %s - %s\n%s", (w['name'], latlon, w['id'], self._strip_html(w['comment'])))
        
        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("set as target")
        button.connect("clicked", self._on_set_coordinate_as_target, None)
        
        p.pack_start(c['coords'], True, True)
        p.pack_start(button, False, True)
        notebook.append_page(p, gtk.Label("coords"))      
        
        # notes
        p = hildon.PannableArea()
        c['notes'] = gtk.TextView()
        #c['notes'].set_editable(True)
        c['notes'].get_buffer().set_text(cache.notes)
        p.add(c['notes'])
        notebook.append_page(p, gtk.Label("notes"))
        
        self.cache_elements = c
        win.add(notebook)
        
        # menu
        menu = hildon.AppMenu()
        c['marked'] = hildon.CheckButton(gtk.HILDON_SIZE_AUTO)
        c['marked'].set_label("marked")
        c['marked'].set_active(cache.marked)
        c['marked'].connect("clicked", self._on_cache_marked_toggle, None)
        menu.append(c['marked'])
        
        
        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("download full details")
        button.connect("clicked", self._on_download_cache_clicked, None)
        menu.append(button)
    
        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("set as target")
        button.connect("clicked", self._on_set_target_clicked, None)
        menu.append(button)
    
        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("log fieldnote")
        button.connect("clicked", self._on_show_log_fieldnote_dialog, None)
        menu.append(button)
        menu.show_all()
        
        win.set_app_menu(menu)        
        win.show_all()
        
    def _on_cache_marked_toggle(self, widget, data):
        if self.current_cache == None:
            return
        self._update_mark(self.current_cache, widget.get_active())
        
    def _on_download_details(self, widget, data):
        pass
        
    def _on_set_as_target(self, widget, data):
        pass
        
    def _on_set_coordinate_as_target(self, widget, data):
        pass
        
        
    def _on_show_log_fieldnote_dialog(self, widget, data):
        if self.current_cache == None:
            return
        
        statuses = [
            ("Don't upload a fieldnote", geocaching.GeocacheCoordinate.LOG_NO_LOG),
            ("Found it", geocaching.GeocacheCoordinate.LOG_AS_FOUND),
            ("Did not find it", geocaching.GeocacheCoordinate.LOG_AS_NOTFOUND),
            ("Post a note", geocaching.GeocacheCoordinate.LOG_AS_NOTE)
        ]
        
        cache = self.current_cache
        dialog = gtk.Dialog("create fieldnote", None, gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        fieldnotes = hildon.TextView()
        fieldnotes.set_placeholder("Your fieldnote text...")
        fieldnotes.get_buffer().set_text(cache.fieldnotes)

        fieldnotes_log_as = gtk.combo_box_new_text()
        for text, status in statuses:
            fieldnotes_log_as.append_text(text)
        i = 0
        for text, status in statuses:
            if cache.log_as == status:
                fieldnotes_log_as.set_active(i)
            i += 1

        dialog.vbox.pack_start(fieldnotes_log_as, False)
        dialog.vbox.pack_start(fieldnotes, True)
        dialog.show_all()
        result = dialog.run()
        dialog.hide()
        if result != gtk.RESPONSE_ACCEPT:
            print 'not logged'
            return
        from time import gmtime
        from time import strftime
        
        cache.logas = statuses[fieldnotes_log_as.get_active()][1]
        cache.logdate = strftime('%Y-%m-%d', gmtime())
        cache.fieldnotes = fieldnotes.get_buffer().get_text(fieldnotes.get_buffer().get_start_iter(), fieldnotes.get_buffer().get_end_iter())

        self.pointprovider.update_field(self.current_cache, 'logas', cache.logas)
        self.pointprovider.update_field(self.current_cache, 'logdate', cache.logdate)
        self.pointprovider.update_field(self.current_cache, 'fieldnotes', cache.fieldnotes)
        
        if cache.logas == geocaching.GeocacheCoordinate.LOG_AS_FOUND:
            self.pointprovider.update_field(self.current_cache, 'found', '1')
            cache.found = 1
            
        elif cache.logas == geocaching.GeocacheCoordinate.LOG_AS_NOTFOUND:
            self.pointprovider.update_field(self.current_cache, 'found', '0')
            cache.found = 0
        


    def _on_marked_label_clicked(self, event=None, widget=None):
        w = xml.get_widget('check_cache_marked')
        w.set_active(not w.get_active())
        print w
    '''
    def _check_notes_save(self):
        if self.current_cache != None and self.notes_changed:
            self.core.on_notes_changed(self.current_cache, self.cache_elements['notes'].get_text(self.cache_elements['notes'].get_start_iter(), self.cache_elements['notes'].get_end_iter()))
            self.notes_changed = False

        if self.current_cache != None and self.fieldnotes_changed:
            self.core.on_fieldnotes_changed(self.current_cache, self.cache_elements['fieldnotes'].get_text(self.cache_elements['fieldnotes'].get_start_iter(), self.cache_elements['fieldnotes'].get_end_iter()))
            self.fieldnotes_changed = False
   '''             
                
                
                
                
                
    # called by core
    '''
    def display_results_advanced(self, caches):
        label = xml.get_widget('label_too_much_results')
        too_much = len(caches) > self.MAX_NUM_RESULTS
        if too_much:
            text = 'Too much results. Only showing first %d.' % self.MAX_NUM_RESULTS
            label.set_text(text)
            label.show()
            caches = caches[:self.MAX_NUM_RESULTS]
        else:
            label.hide()
        self.cachelist_contents = caches
        rows = []
        for r in caches:
            if r.size == -1:
                s = "?"
            else:
                s = "%d" % r.size
                                
            if r.difficulty == -1:
                d = "?"
            else:
                d = "%.1f" % (r.difficulty / 10)
                                
            if r.terrain == -1:
                t = "?"
            else:
                t = "%.1f" % (r.terrain / 10)
            title =  self._format_cache_title(r)
            rows.append((title, r.type, s, t, d, r.name, ))
        self.cachelist.replaceContent(rows)
        self.notebook_search.set_current_page(1)
        self.redraw_marks()

'''

    def set_center(self, coord, noupdate = False):
        SimpleGui.set_center(self, coord, noupdate)
        self.button_center_as_target.set_value("%s %s" % (coord.get_lat(self.format), coord.get_lon(self.format)))
        self.set_active_page(True)

    def hide_progress(self):
        hildon.hildon_gtk_window_set_progress_indicator(self.window, 0)
        self.banner.hide()
        self.banner = None

    def hide_cache_view(self):
        hildon.WindowStack.get_default().pop_1()
        
                
                
    def _on_download_cache_clicked(self, some, thing):
        self.core.on_download_cache(self.current_cache)
        self.hide_cache_view()
        self.show_cache(self.current_cache)
        

    def on_no_fix(self, gps_data, status):
        self.gps_data = gps_data
        self.label_bearing.set_text("No Fix")
        self.label_latlon.set_text(status)
        self.gps_has_fix = False
        self.update_gps_display()
        self._draw_arrow()

                
    def _on_set_target_clicked(self, some, thing):
        if self.current_cache == None:
            return
        
        self.set_target(self.current_cache)
        self.hide_cache_view()

    def _on_set_target_center(self, some, thing):
        self.set_target(self.ts.num2deg(self.map_center_x, self.map_center_y))

                
    def _on_track_toggled(self, something):
        if self.button_track.get_active() and self.gps_data != None and self.gps_data.position != None:
            self.set_center(self.gps_data.position)

    def _on_upload_fieldnotes(self, something):
        self.core.on_upload_fieldnotes()
        
    def on_waypoint_clicked(self, listview, event, element):
        if event.type != gtk.gdk._2BUTTON_PRESS or element == None:
            return
        print element[0]
        if self.current_cache == None:
            return
        if element[0] == 0:
            self.set_target(self.current_cache)
        else:
            wpt = self.current_cache.get_waypoints()[element[0]-1]
            if wpt['lat'] == -1 or wpt['lon'] == -1:
                return
            self.set_target(geo.Coordinate(wpt['lat'], wpt['lon'], wpt['id']))
                
    def on_zoom_changed(self, blub):
        if not self.inhibit_zoom:
            self.zoom()
                
    def _on_zoomin_clicked(self, widget):
        self.zoom( + 1)
                
    def _on_zoomout_clicked(self, widget):
        self.zoom(-1)
                
                
                
    #called by core
    def set_download_progress(self, fraction, text):
        hildon.hildon_gtk_window_set_progress_indicator(self.window, 1)
        if text == '':
            text = 'Please wait...'
        if self.banner == None:
            self.banner = hildon.Banner()
            self.banner.set_text(text)
            self.banner.show_all()
        else:
            self.banner.set_text(text)
        self.do_events()
                
    def set_target(self, cache):
        self.current_target = cache
        coord = "%s %s" % (cache.get_lat(self.format), cache.get_lon(self.format))
        self.label_target.set_value(coord)
        self.button_goto_target.set_value(coord)
        
                

    def show_error(self, errormsg):
        if isinstance(errormsg, Exception):
            raise errormsg
        hildon.hildon_banner_show_information(self.window, None, "%s" % errormsg)

    def show_success(self, message):
        hildon.hildon_banner_show_information(self.window, None, message)
        suc_dlg.run()
        suc_dlg.destroy()
                                
    def update_gps_display(self):
        if self.gps_data == None:
            return

        if self.gps_data.sats == 0:
            label = "No sats available"
        else:
            label = "%d/%d sats, error: ±%3.1fm" % (self.gps_data.sats, self.gps_data.sats_known, self.gps_data.error)
            if self.gps_data.dgps:
                label += " DGPS"
        self.label_quality.set_text(label)
        if self.gps_data.altitude == None or self.gps_data.bearing == None:
            return

        self.label_altitude.set_text("alt %3dm" % self.gps_data.altitude)
        self.label_bearing.set_text("%d°" % self.gps_data.bearing)
        self.label_latlon.set_text("<span size='large'>%s\n%s</span>" % (self.gps_data.position.get_lat(self.format), self.gps_data.position.get_lon(self.format)))
        self.label_latlon.set_use_markup(True)
                
        if self.current_target == None:
            return
                        
        display_dist = self.gps_data.position.distance_to(self.current_target)
                
        target_distance = self.gps_data.position.distance_to(self.current_target)
        if target_distance >= 1000:
            label = "%3dkm" % round(target_distance / 1000)
        elif display_dist >= 100:
            label = "%3dm" % round(target_distance)
        else:
            label = "%2.1fm" % round(target_distance, 1)
        self.label_dist.set_text("<span size='large'>%s</span>" % label)
        self.label_dist.set_use_markup(True)
        
        
                
                
    def write_settings(self, settings):
        self.settings = settings
        self.block_changes = True
        self.ts.set_zoom(self.settings['map_zoom'])
        self.set_center(geo.Coordinate(self.settings['map_position_lat'], self.settings['map_position_lon']))

        return
        if 'last_target_lat' in self.settings.keys():
            self.set_target(geo.Coordinate(self.settings['last_target_lat'], self.settings['last_target_lon'], self.settings['last_target_name']))

        for x in self.SETTINGS_CHECKBOXES:
            if x in self.settings.keys():
                w = xml.get_widget('check_%s' % x)
                if w == None:
                    continue
                w.set_active(self.settings[x])
            elif x in self.DEFAULT_SETTINGS.keys():
                w = xml.get_widget('check_%s' % x)
                if w == None:
                    continue
                w.set_active(self.DEFAULT_SETTINGS[x])
        
        for x in self.SETTINGS_INPUTS:
            if x in self.settings.keys():
                w = xml.get_widget('input_%s' % x)
                if w == None:
                    continue
                w.set_text(str(self.settings[x]))
            elif x in self.DEFAULT_SETTINGS.keys():
                w = xml.get_widget('input_%s' % x)
                if w == None:
                    continue
                w.set_text(self.DEFAULT_SETTINGS[x])
                                        
        self.block_changes = False
                
    def zoom(self, direction=None):
        size = self.ts.tile_size()
        center = self.ts.num2deg(self.map_center_x - float(self.draw_at_x) / size, self.map_center_y - float(self.draw_at_y) / size)
        if direction == None:
            #newzoom = self.zoom_adjustment.get_value()
            print "not"
        else:
            newzoom = self.ts.get_zoom() + direction
        self.ts.set_zoom(newzoom)
        self.set_center(center)
             