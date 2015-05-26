openerp.clinic = function(instance) {
    instance.web_calendar.CalendarView.include({
        get_fc_init_options: function () {
            //Documentation here : http://arshaw.com/fullcalendar/docs/
            var self = this;
            return  $.extend({}, get_fc_defaultOptions(), {
                
                defaultView: (this.mode == "month")?"month":
                    (this.mode == "week"?"agendaWeek":
                     (this.mode == "day"?"agendaDay":"month")),
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month,agendaWeek,agendaDay'
                },
                selectable: !this.options.read_only_mode && this.create_right,
                selectHelper: true,
                editable: !this.options.read_only_mode,
                droppable: true,
                contentHeight: 600,
                // TODO hacer customizables nuestras opciones
                slotMinutes: 15,
                firstHour: 8,
                // defaultEventMinutes: 120,
                // minTime: 0,
                // maxTime: 24,

                // callbacks

                eventDrop: function (event, _day_delta, _minute_delta, _all_day, _revertFunc) {
                    var data = self.get_event_data(event);
                    self.proxy('update_record')(event._id, data); // we don't revert the event, but update it.
                },
                eventResize: function (event, _day_delta, _minute_delta, _revertFunc) {
                    var data = self.get_event_data(event);
                    self.proxy('update_record')(event._id, data);
                },
                eventRender: function (event, element, view) {
                    element.find('.fc-event-title').html(event.title);
                },
                eventAfterRender: function (event, element, view) {
                    if ((view.name !== 'month') && (((event.end-event.start)/60000)<=30)) {
                        //if duration is too small, we see the html code of img
                        var current_title = $(element.find('.fc-event-time')).text();
                        var new_title = current_title.substr(0,current_title.indexOf("<img")>0?current_title.indexOf("<img"):current_title.length);
                        element.find('.fc-event-time').html(new_title);
                    }
                },
                eventClick: function (event) { self.open_event(event._id,event.title); },
                select: function (start_date, end_date, all_day, _js_event, _view) {
                    var data_template = self.get_event_data({
                        start: start_date,
                        end: end_date,
                        allDay: all_day,
                    });
                    self.open_quick_create(data_template);

                },

                unselectAuto: false,


            });
        },
    }
    )
}