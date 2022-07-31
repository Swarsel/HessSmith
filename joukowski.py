import numpy as np
import matplotlib.pyplot as plt
from math import atan2, pow




def karman_trefftz_transform(zeta, n):
    z = n * ((zeta + 1) ** n + (zeta - 1) ** n) / ((zeta + 1) ** n - (zeta - 1) ** n)
    return z


def make_karman_trefftz(mux=0.2, muy=0.1, n=1.9, N=100):
    t0 = -mux + muy * 1j  # center
    R = np.sqrt((1 + mux) ** 2 + muy ** 2)  # radius

    theta = np.linspace(0, 2 * np.pi, N)
    Xc = np.real(t0) + R * np.cos(theta)
    Yc = np.imag(t0) + R * np.sin(theta)
    tx = np.real(t0)
    ty = np.imag(t0)

    p = karman_trefftz_transform(Xc + Yc * 1j, n)
    Xp, Yp = np.real(p), np.imag(p)
    return Xp, Yp, R, muy

def joukowski_transfrom(zeta):
    z = zeta + 1 / zeta
    return z

def make_joukowski(mux=0.2, muy=0.1, N=100):
    center = -mux + muy * 1j  # center
    R = np.sqrt((1 + mux) ** 2 + muy ** 2)  # radius

    theta = np.linspace(0, 2 * np.pi, N)
    Xc = np.real(center) + R * np.cos(theta)
    Yc = np.imag(center) + R * np.sin(theta)

    p = joukowski_transfrom(Xc + Yc * 1j)
    Xp, Yp = np.real(p), np.imag(p)
    return Xp, Yp, R, muy


def joukowski_ca(a, R, muy, t):
    a = np.radians(a)
    return (8 * R * np.pi * np.sin(a + np.arcsin(muy/R)))/t

def make_joukowski_all(mux=0.2, muy=0.1, N=100):
    t0 = -mux + muy * 1j  # center
    R =  np.sqrt((1 + mux) ** 2 + muy ** 2)  # radius
    Rci = np.sqrt((-1 + -mux) ** 2 + muy ** 2)# radius

    theta = np.linspace(0, 2 * np.pi, N)
    Xc = np.real(t0) + R * np.cos(theta)
    Yc = np.imag(t0) + R * np.sin(theta)
    tx = np.real(t0)
    ty = np.imag(t0)

    p = joukowski_transfrom(Xc + Yc * 1j)
    Xp, Yp = np.real(p), np.imag(p)
    return Xp, Yp, Xc, Yc, tx, ty, muy, mux, R, Rci

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
