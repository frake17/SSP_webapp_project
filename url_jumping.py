from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint


def check_role(role):  # SSP CODE DONE BY KIN
    current_role = session.get('role', None)
    if current_role != role:
        session['access denied'] = 'Access to this page is denied'
        return False
    else:
        return True
