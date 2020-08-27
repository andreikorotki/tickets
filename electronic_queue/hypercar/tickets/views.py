from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect

line_of_cars = {'change_oil': [], 'inflate_tires': [],
                'diagnostic': [], 'counter': 0}
# counters = {'change_oil': 0, 'inflate_tires': 0, 'diagnostic': 0}

processed_tickets = []

class WelcomeView(View):
    html = '<html lang="en"><head>' \
           '<meta charset="UTF-8"><title>Welcome Page</title></head><body>' \
           '<h2>Welcome to the Hypercar Service!</h2></body></html>'

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.html)


def menu(request):
    return render(request, 'menu.html')


def get_est_time_waiting(request_type):
    req_operation = str(request_type).lower()
    req_op_time = settings.HYPERCAR_OPERATIONS.get(req_operation)
    est_time = 0

    for operation_key, op_time in settings.HYPERCAR_OPERATIONS.items():
        if op_time <= req_op_time:
            est_time += len(line_of_cars.get(operation_key)) * op_time
    return est_time


def increase_counter():
    cur_value = line_of_cars['counter']
    cur_value += 1
    line_of_cars['counter'] = cur_value
    return cur_value


def add_request(request_type):
    ticket_num = increase_counter()
    line_of_cars.get(str(request_type).lower()).insert(0, ticket_num)
    return ticket_num


def get_next_ticket():
    sorted_dict = sorted(settings.HYPERCAR_OPERATIONS.items(), key=lambda kv: kv[1])
    operation_key = ''
    op_time = 0
    ticket_number = 0
    for operation_key, op_time in sorted_dict:
        if len(line_of_cars.get(operation_key)) > 0:
            ticket_number = line_of_cars.get(operation_key)[-1]
            break
    return {'operation': operation_key,
            'ticket_number': ticket_number,
            'time': op_time}


def get_next_next_ticket():
    sorted_dict = sorted(settings.HYPERCAR_OPERATIONS.items(), key=lambda kv: kv[1])
    operation_key = ''
    op_time = 0
    ticket_number = 0
    counter = 0
    for operation_key, op_time in sorted_dict:
        if len(line_of_cars.get(operation_key)) > 0:
            if len(line_of_cars.get(operation_key)) > 1:
                ticket_number = line_of_cars.get(operation_key)[-2]
                break
            else:
                if counter == 1:
                    ticket_number = line_of_cars.get(operation_key)[-1]
                    break
                counter = 1
    return {'operation': operation_key,
            'ticket_number': ticket_number,
            'time': op_time}


def change_oil(request):
    est_time = get_est_time_waiting('change_oil')
    ticket_num = add_request('change_oil')
    return render(request, 'change_oil.html', {'ticket_number': ticket_num,
                                               'minutes_to_wait': est_time})


def inflate_tires(request):
    est_time = get_est_time_waiting('inflate_tires')
    ticket_num = add_request('inflate_tires')
    return render(request, 'inflate_tires.html', {'ticket_number': ticket_num,
                                                  'minutes_to_wait': est_time})


def diagnostic(request):
    est_time = get_est_time_waiting('diagnostic')
    ticket_num = add_request('diagnostic')
    return render(request, 'diagnostic.html', {'ticket_number': ticket_num,
                                               'minutes_to_wait': est_time})


def processing(request):
    if request.method == 'GET':
      len_change_oil = len(line_of_cars.get('change_oil'))
      len_inflate_tires = len(line_of_cars.get('inflate_tires'))
      len_diagnostic = len(line_of_cars.get('diagnostic'))
      return render(request, 'processing.html',
                    {'len_change_oil': len_change_oil,
                     'len_inflate_tires': len_inflate_tires,
                     'len_diagnostic': len_diagnostic})
    else:
        next_ticket = get_next_ticket()
        if next_ticket['ticket_number'] > 0:
            processed_tickets.append(next_ticket)
            line_of_cars.get(next_ticket.get('operation')).pop()
        return HttpResponseRedirect('/processing')


def next_ticket(request):
    if len(processed_tickets) > 0:
        last_ticket = processed_tickets[-1]
    else:
        last_ticket = {'operation': 0,
                        'ticket_number': 0,
                        'time': 0}
    return render(request, 'next.html', {'last_ticket': last_ticket})


