#include "solver.h"
#include "Functions.h"
#include <iostream>
/*
�������:

Solver Sol(num_intervals, TEST); - ������ ������� (����� ���������� �����, ��� ������)
    ���� �����:
    TEST - ��������
    MAIN1 - 1 ������� (�������� � ����� �� ���� ����� ��������)
    MAIN2 - 2 �������
    MAIN3 - 3 �������
    MAIN4 - 4 �������
    OSC - ������������� 

����� ������� ����� ��� ����������
    1 ������� ����������� �� num_nodes ��� ��� ��� ����� �������:
    getA()
    getB()
    getC()
    getD() - ��� �� ��� ���������� ������������� (���������� ������)
    getX_for_coef_table() - ������������ ���� (������)
    get_n_step() - ���������� ���, � ������� ��� �� �������� �����(�� , ����� � �� �����)

    2 � 3 ������� : (����������� �� num_nodes*2 ��� ��� ��� ����������� �����)
    getX() - ������������ ���� (������)
    getF()
    getDF()
    getD2F()
    getS()
    getDS()
    getD2S() - ��� �� ������� �������� ������� � ������� ������� F - �������� S - �������,
               D � D2 - �� �����������
    get_N_step() - ���������� ���, � ������� ��� �� �������� �����(�� , ����� � �� �����)

    �������:
    getF_ERRROR();
    getF_ERRROR_X();
    getDF_ERRROR();
    getDF_ERRROR_X();
    getD2F_ERRROR();
    getD2F_ERRROR_X(); - ��� ���������� ������������ ����������� � �������������� �� x;

*/

int main() {
   
    int num_intervals{ 5 };
    Solver Sol(num_intervals, MAIN1);
    Sol.Solve();
    
    auto f = Sol.getF();
    auto s = Sol.getS();
    //���� ������� ��� �������� ��� ������ ������

    return 0;
}