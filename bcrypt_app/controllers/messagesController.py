from flask import Flask, request, redirect, render_template, session, flash
from bcrypt_app import app
from bcrypt_app.models import messageModel, userModel, reportModel
import socket

@app.route('/send/to/<int:receiverId>/from/<int:senderId>', methods=['POST'])
def send(senderId, receiverId):

    data = {
        'receiverId': receiverId,
        'senderId': senderId,
        'message': request.form['message']
    }

    if not messageModel.Message.validateMessage(data):
        return redirect('/dashboard')

    messageModel.Message.save(data)
    return redirect('/dashboard')

def getLocalIP():
    newSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    newSocket.connect(('google.com', 80))
    return newSocket.getsockname()[0]

@app.route('/delete/<int:messageId>', methods=['POST'])
def delete(messageId):
    data = {
        'messageId': messageId
    }

    if 'userId' in session:
        userId = session['userId']

        message = messageModel.Message.findMessageById(data)

        print(f'userId: {userId} message receiver_id {message.receiver_id} message sender_id {message.sender_id}')

        if message != None:
            if message.receiver_id != int(userId) and message.sender_id != int(userId):
                
                # Sólo trae 127.0.0.1
                # if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                #     ip = request.environ['REMOTE_ADDR']
                # else:
                #     ip = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

                reportData = {
                    'userId': userId,
                    'userIp': getLocalIP() # Obtiene IP de Equipo
                }

                # Guardar Reporte con IP
                reportModel.Report.save(reportData)
                # Buscar reportes previos de usuario
                reports = reportModel.Report.get_all_by_userId(reportData)

                if reports != None:
                    if len(reports) == 1:
                        return redirect('/danger')
                    elif len(reports) > 1:
                        userModel.User.blockUser(reportData)
                        session.pop('userId')
                        return redirect('/blocked')

                return redirect('/')
            else:
                messageModel.Message.deleteLogically(data)
                flash(f'Message with id {messageId} was deleted', 'delete_success')
                return redirect('/dashboard')
        else:
            flash(f'Message with id {messageId} was not found', 'delete_error')
            return redirect('/dashboard')

    # Session no contiene usuario logueado
    else:
        return redirect('/logout')

@app.route('/danger', methods=['GET'])
def danger():
    if 'userId' in session:
        userId = session['userId']

        data = {
            'userId': userId
        }

        report = reportModel.Report.findLastReportByUserId(data)

    return render_template('danger.html', report = report)

@app.route('/blocked', methods=['GET'])
def blocked():
    return render_template('blocked.html')
