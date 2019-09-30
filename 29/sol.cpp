#!/bin/bash

TMPSRC=tmp.cpp
TMPSRCEXE=${TMPSRC}.exe
python -c "import sys; print sys.stdin.read().split('===' + '+++' + '===')[1]" < $0 > $TMPSRC
g++ -O3 -std=c++17 $TMPSRC -o $TMPSRCEXE
echo "Compilation finished" >&2
exec ./$TMPSRCEXE

===+++===
#line 12 "sol.cpp"

#include <iostream>
#include <algorithm>
#include <cstdio>
#include <vector>
#include <set>

std::vector<char> letters = {'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'};

std::vector<std::vector<int>> penaltyByIdxs = {
	{4, 0, -2, -1, -2, 0, -2, -1, -1, -1, -1, -2, -1, -1, -1, 1, 0, 0, -3, -2},
	{0, 9, -3, -4, -2, -3, -3, -1, -3, -1, -1, -3, -3, -3, -3, -1, -1, -1, -2, -2},
	{-2, -3, 6, 2, -3, -1, -1, -3, -1, -4, -3, 1, -1, 0, -2, 0, -1, -3, -4, -3},
	{-1, -4, 2, 5, -3, -2, 0, -3, 1, -3, -2, 0, -1, 2, 0, 0, -1, -2, -3, -2},
	{-2, -2, -3, -3, 6, -3, -1, 0, -3, 0, 0, -3, -4, -3, -3, -2, -2, -1, 1, 3},
	{0, -3, -1, -2, -3, 6, -2, -4, -2, -4, -3, 0, -2, -2, -2, 0, -2, -3, -2, -3},
	{-2, -3, -1, 0, -1, -2, 8, -3, -1, -3, -2, 1, -2, 0, 0, -1, -2, -3, -2, 2},
	{-1, -1, -3, -3, 0, -4, -3, 4, -3, 2, 1, -3, -3, -3, -3, -2, -1, 3, -3, -1},
	{-1, -3, -1, 1, -3, -2, -1, -3, 5, -2, -1, 0, -1, 1, 2, 0, -1, -2, -3, -2},
	{-1, -1, -4, -3, 0, -4, -3, 2, -2, 4, 2, -3, -3, -2, -2, -2, -1, 1, -2, -1},
	{-1, -1, -3, -2, 0, -3, -2, 1, -1, 2, 5, -2, -2, 0, -1, -1, -1, 1, -1, -1},
	{-2, -3, 1, 0, -3, 0, 1, -3, 0, -3, -2, 6, -2, 0, 0, 1, 0, -3, -4, -2},
	{-1, -3, -1, -1, -4, -2, -2, -3, -1, -3, -2, -2, 7, -1, -2, -1, -1, -2, -4, -3},
	{-1, -3, 0, 2, -3, -2, 0, -3, 1, -2, 0, 0, -1, 5, 1, 0, -1, -2, -2, -1},
	{-1, -3, -2, 0, -3, -2, 0, -3, 2, -2, -1, 0, -2, 1, 5, -1, -1, -3, -3, -2},
	{1, -1, 0, 0, -2, 0, -1, -2, 0, -2, -1, 1, -1, 0, -1, 4, 1, -2, -3, -2},
	{0, -1, -1, -1, -2, -2, -2, -1, -1, -1, -1, 0, -1, -1, -1, 1, 5, 0, -2, -2},
	{0, -1, -3, -2, -1, -3, -3, 3, -2, 1, 1, -3, -2, -2, -3, -2, 0, 4, -3, -1},
	{-3, -2, -4, -3, 1, -2, -2, -3, -3, -2, -1, -4, -4, -2, -3, -3, -2, -3, 11, 2},
	{-2, -2, -3, -2, 3, -3, 2, -1, -2, -1, -1, -2, -3, -1, -2, -2, -2, -1, 2, 7},
};

std::vector<std::vector<int>> penalty = std::vector<std::vector<int>>(256, std::vector<int>(256));

struct TPos {
    int A;
    int B;
};

struct TCPair {
    char A;
    char B;
};

struct TCell {
    int D;
    TCPair CP;
};

using TRow = std::vector<TCell>;


TRow CalcRow(const TRow& prevRow, char curA, const std::string& b) {
    auto row = TRow(prevRow.size());
    row[0] = {prevRow[0].D - 5, {curA, '-'}};
    for (size_t i = 0; i < b.size(); ++i) {
        auto [nd, na, nb] = std::max(
            std::tuple{prevRow[i].D + penalty[curA][b[i]], curA, b[i]},
            std::max(
                std::tuple{prevRow[i + 1].D + penalty[curA]['-'], curA, '-'},
                std::tuple{row[i].D + penalty['-'][b[i]], '-', b[i]}
            )
        );
        row[i + 1] = {nd, {na, nb}};
    }
    return row;
}

std::tuple<int, std::string, std::string> Solve(const std::string& a, const std::string& b) {
    std::vector<TRow> d(a.size() + 2, TRow(b.size() + 2));
    auto& frow = d[0];
    frow[0] = {0, {'-', '-'}};
    for (size_t i = 0; i < b.size(); ++i) {
        frow[i + 1] = {frow[i].D - 5, {'-', b[i]}};
    }
    for (size_t i = 0; i < a.size(); ++i) {
        d[i + 1] = CalcRow(d[i], a[i], b);
    }


    std::string sa, sb;
    TPos pos = {(int)a.size(), (int)b.size()};
    while (pos.A != 0 || pos.B != 0) {
        auto& pd = d[pos.A][pos.B];
        sa.push_back(pd.CP.A);
        sb.push_back(pd.CP.B);
        pos = {pos.A - (pd.CP.A != '-'), pos.B - (pd.CP.B != '-')};
    }
    std::reverse(sa.begin(), sa.end());
    std::reverse(sb.begin(), sb.end());
    return {d[a.size()][b.size()].D, sa, sb};
}

std::tuple<int, std::string, std::string> SolveBig(const std::string& a, const std::string& b) {
    std::vector<TRow> d(a.size() + 2, TRow());
    d[0] = TRow(b.size() + 2);
    auto& frow = d[0];
    frow[0] = {0, {'-', '-'}};
    for (size_t i = 0; i < b.size(); ++i) {
        frow[i + 1] = {frow[i].D - 5, {'-', b[i]}};
    }

    auto doRow = [&](int posA) {
        int prevCalculated = posA;
        while (d[prevCalculated].size() == 0) {
            --prevCalculated;
        }
        while (prevCalculated < posA) {
            int delta = posA - prevCalculated;
            int step = 1;
            while (step * 2 <= delta) {
                step *= 2;
            }
            for (int i = prevCalculated + 1; i <= prevCalculated + step; ++i) {
                d[i] = CalcRow(d[i - 1], a[i - 1], b);
                if (i != prevCalculated + 1) {
                    d[i - 1] = {};
                }
            }
            prevCalculated += step;
        }
    };
    //~ for (size_t i = 0; i < a.size(); ++i) {
        //~ d[i + 1] = CalcRow(d[i], a[i], b);
    //~ }


    std::string sa, sb;
    TPos pos = {(int)a.size(), (int)b.size()};
    while (pos.A != 0 || pos.B != 0) {
        d[pos.A + 1].clear();
        doRow(pos.A);
        auto& pd = d[pos.A][pos.B];
        sa.push_back(pd.CP.A);
        sb.push_back(pd.CP.B);
        pos = {pos.A - (pd.CP.A != '-'), pos.B - (pd.CP.B != '-')};
    }
    std::reverse(sa.begin(), sa.end());
    std::reverse(sb.begin(), sb.end());
    return {d[a.size()][b.size()].D, sa, sb};
}

int main() {
    for (size_t i = 0; i < letters.size(); ++i) {
        for (size_t j = 0; j < letters.size(); ++j) {
            penalty[letters[i]][letters[j]] = penaltyByIdxs[i][j];
        }
        penalty[letters[i]]['-'] = -5;
        penalty['-'][letters[i]] = -5;
    }

    std::string a, b;
    std::cin >> a >> b;
    //~ {
        //~ auto [score, sa, sb] = Solve(a, b);
        //~ std::cout << score << std::endl << sa << std::endl << sb << std::endl;
    //~ }
    {
        auto [score, sa, sb] = SolveBig(a, b);
        std::cout << score << std::endl << sa << std::endl << sb << std::endl;
    }
    return 0;
}
