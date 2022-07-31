import numpy as np
import matplotlib.pyplot as plt
from math import atan2, pow


def joukowski_transfrom(a, z):
    zeta = z + a ** 2 / z
    return zeta


def joukowski_transfrom_alt(zeta):
    z = zeta + 1 / zeta
    return z


def karman_trefftz_transform(zeta, n):
    z = n * ((zeta + 1) ** n + (zeta - 1) ** n) / ((zeta + 1) ** n - (zeta - 1) ** n)
    return z


def make_karman_trefftz(mux=0.2, muy=0.1, n=1.9, N=100):
    t0 = (-mux + muy * 1j)  # center
    R = np.sqrt((1 + mux) ** 2 + muy ** 2)  # radius

    theta = np.linspace(0, 2 * np.pi, N)
    Xc = np.real(t0) + R * np.cos(theta)
    Yc = np.imag(t0) + R * np.sin(theta)
    tx = np.real(t0)
    ty = np.imag(t0)

    p = karman_trefftz_transform(Xc + Yc * 1j, n)
    Xp, Yp = np.real(p), np.imag(p)
    return Xp, Yp

def make_karman_trefftz_all(mux=0.2, muy=0.1, n=1.9, N=100):
    t0 = (-mux + muy * 1j)  # center
    R = np.sqrt((1 + mux) ** 2 + muy ** 2)  # radius

    theta = np.linspace(0, 2 * np.pi, N)
    Xc = np.real(t0) + R * np.cos(theta)
    Yc = np.imag(t0) + R * np.sin(theta)
    tx = np.real(t0)
    ty = np.imag(t0)

    p = karman_trefftz_transform(Xc + Yc * 1j, n)
    Xp, Yp = np.real(p), np.imag(p)
    return Xp, Yp, Xc, Yc, tx, ty, muy, mux

def make_joukowski_allt(lamda=0.2, delta=0.1, a=1, N=100):
    t0 = a * (-lamda + delta * 1j)  # center
    R = a * np.sqrt((1 + lamda) ** 2 + delta ** 2)  # radius
    Rci = a * np.sqrt((-1 + -lamda) ** 2 + delta ** 2)# radius

    theta = np.linspace(0, 2 * np.pi, N)
    Xc = np.real(t0) + R * np.cos(theta)
    Yc = np.imag(t0) + R * np.sin(theta)
    tx = np.real(t0)
    ty = np.imag(t0)

    p = joukowski_transfrom(a, Xc + Yc * 1j)
    Xp, Yp = np.real(p), np.imag(p)
    return Xp, Yp, Xc, Yc, tx, ty, delta, lamda, Rci, R

def make_joukowski_all(lamda=0.2, delta=0.1, a=1, N=100):
    t0 = a * (-lamda + delta * 1j)  # center
    R = a * np.sqrt((1 + lamda) ** 2 + delta ** 2)  # radius
    Rci = a * np.sqrt((-1 + -lamda) ** 2 + delta ** 2)# radius

    theta = np.linspace(0, 2 * np.pi, N)
    #print(theta)
    Xc = np.real(t0) + R * np.cos(theta)
    Yc = np.imag(t0) + R * np.sin(theta)
    tx = np.real(t0)
    ty = np.imag(t0)

    p = joukowski_transfrom(a, Xc + Yc * 1j)
    Xp, Yp = np.real(p), np.imag(p)
    return Xp, Yp, Xc, Yc, tx, ty, delta, lamda, R, Rci


def make_joukowski(lamda=0.2, delta=0.1, a=1, N=100):
    t0 = a * (-lamda + delta * 1j)  # center
    R = a * np.sqrt((1 + lamda) ** 2 + delta ** 2)  # radius

    theta = np.linspace(0, 2 * np.pi, N)
    Xc = np.real(t0) + R * np.cos(theta)
    Yc = np.imag(t0) + R * np.sin(theta)

    p = joukowski_transfrom(a, Xc + Yc * 1j)
    Xp, Yp = np.real(p), np.imag(p)
    return Xp, Yp,


def karman_trefftz(lamda=0.2, delta=0.1, a=1, N=100):
    t0 = a * (-lamda + delta * 1j)  # center
    R = a * np.sqrt((1 + lamda) ** 2 + delta ** 2)

    theta = np.linspace(0, 2 * np.pi, N)
    Xc = np.real(t0) + R * np.cos(theta)
    Yc = np.imag(t0) + R * np.sin(theta)
    zeta = joukowski_transfrom(a, Xc + Yc * 1j)

def joukowski_ca(a, R, muy, t):
    return (8  * np.pi * R * np.sin(a + np.arcsin(muy/R)))/t
