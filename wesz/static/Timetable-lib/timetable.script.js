window.onload = function() {
}

function createTimetable(date)
{
    window.timetable.events = [];
    for(var i = 0; i < window.reservations.length; i++)
    {
        ev = window.reservations[i];
        if(ev.beginDate.toDateString() != date.toDateString()) continue;
        window.timetable.addEvent(ev.group, ev.room + "", ev.beginDate, ev.endDate);
    }

    var renderer = new Timetable.Renderer(window.timetable);
    renderer.draw('.timetable');
}
