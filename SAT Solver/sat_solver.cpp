#include <bits/stdc++.h>
#include <fstream>
#include  <iostream>
using namespace std;

vector<int>result;

//to return the clause number with the least number of literals
int s_clause(vector<vector<int>> clauses){
    int min=0;
    
    for(int i =0;i<clauses.size();i++){
        if(clauses[i].size()<clauses[min].size()){
            min =i;
        }
    }

    return min;
}

//to return the index of the maximum occurred literal out of the smallest clause so chosen
//positive if truth value initialy maximum occurring taken is true else negetive
int m_o_p(vector<vector<int>>clauses,int smallest_clause){
    int len = clauses[smallest_clause].size();
    int i,j,k;
    vector<int> prop_pos(len+1,0);
    vector<int> prop_neg(len+1,0);

    for(i =0;i<clauses.size();i++){
        for(j=0;j<clauses[i].size();j++){
            for(k=1;k<len+1;k++){
                if(clauses[i][j]==clauses[smallest_clause][k]){
                    prop_pos[k]++;
                    break;
                }
                else if((-1)*clauses[i][j]==clauses[smallest_clause][k]){
                    prop_neg[k]++;
                    break;
                }
            }
        }
    }

    i=1;
    for(k=1;k<len+1;k++){
        if(prop_pos[k] + prop_neg[k] > prop_pos[i] + prop_neg[i]) i=k;
    }
    
    if(prop_pos[i] >= prop_neg[i]){
        return i-1;
    }
    else{
        return -i+1;
    }
}

//to change clauses after setting a truth value to a literal, here say m_prop
vector<vector<int>> trim(vector<vector<int>> clauses, int m_prop){
    int i,j;
    vector<int>arr;
    for(i =0;i<clauses.size();i++){
        for(j=0;j<clauses[i].size();j++){
            //for the clause with same truth value as m_prop as one of the literal, the clause is erased after keeping a record the clauses to be removed
            if(clauses[i][j]==m_prop){
                arr.push_back(i); 
                break;
            }
            //for the clause with the negation of truth value of m_prop, the literal is removed from the clause
            else if(clauses[i][j]==m_prop*(-1)){
                clauses[i].erase(clauses[i].begin()+j);
                break;
            }
        }
    }

    for(i=0;i<arr.size();i++){
        clauses.erase(clauses.begin()+arr[i]-i);
    }

    return clauses;
}

//the function to return 1 in case of satisfiability and 0 in case of Unsatisfiability
int solve(vector<vector<int>> clauses){
    //recurrsive function for backtracking as well as setting a model
    int len= clauses.size(); //the length of clause at this point
    if(len==0) return 1; //no clauses left to check thus got a sat condition
    
    int smallest_clause = s_clause(clauses); //to return the clause of smallest length
    if(clauses[smallest_clause].size()==0) return 0; //the clause has got contradiction thus unsat
    
    int max_occ_prop = m_o_p(clauses,smallest_clause); //the index of the maximum occurred literal out of the smallest clause so chosen
    int m_prop; 
    
    //to store initial maximum occured literal, positive if truth value initialy taken is true else negetive
    if(max_occ_prop>0) m_prop=(clauses[smallest_clause][max_occ_prop]);
    else{
        m_prop=(-1)*(clauses[smallest_clause][max_occ_prop*(-1)]);
    }
    result.push_back(m_prop);//appending the literal with truth value as solution
    
    //trim the prop from clauses and checking if it has got solution
    if(solve(trim(clauses,m_prop))){
        return 1;
    }
    else{
        //no solution then poping the literal and appending back the negation
        result.pop_back();
        result.push_back((-1)*m_prop);
        if(solve(trim(clauses,(-1)*m_prop))==1){
            return 1; //got sat result
        }
        else{
            //got unsat result
            result.pop_back();
            return 0;
        }
    }
}

int main()
{
    clock_t tStart = clock();//start time

    vector<vector<int>> clauses;
    int clausesno; //to store number of clauses to be appended
    int i, j;
    int literals; //to store number of variables

    cout << "Please enter input cnf file path to get its satisfibility: ";
    string myfile;
    getline(cin, myfile);//taking cnf file as input
    ifstream ifs(myfile.c_str());
    if (!ifs) printf("can't open input file");

    string line, cnfl;
    while (getline(ifs, line))
    {
        int number;
        if (line[0] != 'c')
        {
            if (line[0] == 'p')
            {
                vector<int> v;
                cnfl = line.substr(6);
                stringstream iss(cnfl);
                while (iss >> number)
                    v.push_back(number);
                literals = v[0];
                clausesno = v[1];
                v.clear();
            }
            else
            {
                stringstream iss(line);
                vector<int> v;
                while (iss >> number && number != 0)
                {
                    v.push_back(number);
                }
                clauses.push_back(v); //appending each clause in clauses
            }
        }
    }
    ifs.close();

    int is_sat = solve(clauses);

    //output of a model if the formula is satisfiable and report that the formula is unsatisfiable

    cout << "Please enter the txt file path to get its output: ";
    string outfile;
    getline(cin, outfile);//taking cnf file as input
    ofstream out_file(outfile.c_str());
    if (!out_file) printf("can't open ouput file");

	// ofstream out_file;
	// out_file.open("output.txt");
	if(is_sat==1){
		out_file<<"SAT\n";
		//if some literal is not in solution, then it can take any value, here we give it a true value 
        for(i=1;i<=literals;i++){
            if(!((count(result.begin(),result.end(),i)||(count(result.begin(),result.end(),-i))))){
                result.push_back(i);
            }
        }
		sort(result.begin(), result.end(), [](auto & l, auto & r){return abs(l)<abs(r);}); //sorting as per absolute value
        for(i=0;i<result.size();i++){
            out_file<<result[i]<<" ";
        }
		out_file<<"0";
	}
	else{
	out_file<<"UNSAT";	
	}
	out_file.close();

    printf("Time taken: %.2fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);

    return 0;
}