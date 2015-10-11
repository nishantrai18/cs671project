#include <iostream>
#include <algorithm>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <map>
#include <vector>
#define MAX_STRING 100

using namespace std;

vector<double> operator+(const vector<double>& v1, const vector<double>& v2)
{
    vector <double> tmp;
    for (int i=0;i<v1.size();i++)
    {
        tmp.push_back(v1[i]+v2[i]);
    }
    return tmp;
}

vector<double> operator-(const vector<double>& v1, const vector<double>& v2)
{
    vector <double> tmp;
    for (int i=0;i<v1.size();i++)
    {
        tmp.push_back(v1[i]-v2[i]);
    }
    return tmp;
}

vector<double> operator/(const vector<double>& v1, const double& num)
{
    vector <double> tmp;
    for (int i=0;i<v1.size();i++)
    {
        tmp.push_back(v1[i]/num);
    }
    return tmp;
}

map <string, vector <double> > wordvec;

struct sense{
	int senseNumber;
	vector <double> senseVector;
	vector <double> center;
	double size;
};

struct senseList{
	int totalSenses;
	vector <sense> senses;
	double size;
};

void ReadWord(string &word, FILE *fin) {
  int a = 0;
  char ch;
  word = "";
  while (!feof(fin)) {
    ch = fgetc(fin);
    if (ch == 13) continue;
    if ((ch == ' ') || (ch == '\t') || (ch == '\n')) {
      if (a > 0) {
        if (ch == '\n') ungetc(ch, fin);
        break;
      }
      if (ch == '\n') {
        word = "</s>";
        return;
      } else continue;
    }
    word += ch;
    a++;
    if (a >= MAX_STRING - 1)
    {
      a--;   // Truncate too long words
      return;
    }
  }
}

void InitNULL(vector <double>& tmp, int size)
{
    tmp.resize(size);
    for(int i=0;i<size;i++)
        tmp[i]=0;
}

double similarity(vector <double> arr, vector <double> bar)
{
    double a=0,b=0,c=0;
    int i=0;
    for(i=0;i<arr.size();i++)
    {
        c += arr[i]*bar[i];
        a += arr[i]*arr[i];
        b += bar[i]*bar[i];
    }
    return (c/(sqrt(a)*sqrt(b)));
}

int main()
{
    int maxWindowSize = 5, dim = 100;
    double threshold = -0.5;

    /*

    INPUT WORD VECTORS PART A..... INPUT VOCABULARY..... SELECT TOP 1000-10000 words for clustering

    ASSUME wordvec contains word vectors of all words

    */

    FILE* fi = fopen("vectors.bin","r");

    //Format is Number of words, Dimension 
    //string d doubles 
    int numWords;

    int i,j,t,w=0;

    cout<<"SUCCESS\n";

    fscanf(fi,"%d%d",&numWords,&dim);

    cout<<numWords<<dim<<endl;

    for(i=0 ; i < numWords ; i++)
    {
        char str[110];
        fscanf(fi,"%s",str);
        string tmp = string(str);
        vector <double> vec;
        vec.resize(dim);
        for(j=0;j<dim;j++)
            fscanf(fi,"%lf",&vec[j]);
        wordvec.insert(make_pair(tmp,vec));
        if(i%10000==0)
            cout<<i<<endl;

    }

    fclose(fi);

    cout<<"SUCCESS\n";

    FILE* fo = fopen("SOMEFILE","r");
    vector < vector <string> > sent;
    vector < vector <double> > contvec;
    vector <int> senseID;

    int cnt=0, totalWords=0;
    sent.resize(++cnt);
    while(1)
    {
        string word;
        ReadWord(word, fo);
        if(feof(fo))
            break;
        if(word == "</s>")
            sent.resize(++cnt);
        sent[cnt].push_back(word);
        totalWords++;
    }

    fclose(fo);

    contvec.resize(totalWords+10);
    senseID.resize(totalWords+10);
    
    for(i=0;i<sent.size();i++)
    {
        for(j=0;j<sent[i].size();j++)
        {
            int window = rand()%maxWindowSize+1, cnt = 0;
            InitNULL(contvec[w],dim);
            for(int k = j-window ; k <= (j+window) ; k++)
            {
                if(k<0)
                    contvec[w]=contvec[w]+wordvec["</s>"];
                else if(k>=sent[i].size())
                    contvec[w]=contvec[w]+wordvec["</s>"];
                else if(wordvec.find(sent[i][j])==wordvec.end())
                    continue;
                else if(k != j)
                    contvec[w]=contvec[w]+wordvec[sent[i][j]];
                cnt++;
            }
            contvec[w] = contvec[w]/(cnt*(1.0));
            w++;
        }
    }

    senseList clust;
    
    int clt=0;
    clust.totalSenses = 0;
    (clust.senses).resize(++clt);
    InitNULL((clust.senses[clt-1]).center,dim);

    for(i=0;i<contvec.size();i++)
    {
        int id=0;
        double maxa = -10000;
        for(j=0;j<clt;j++)
        {   
            double sim = similarity(contvec[i],(clust.senses[j]).center);
            if(sim>maxa)
            {
                maxa = sim;
                id = j;
            }
        }
        if(maxa < threshold)                                                                                //Define some threshold, discrete model for now
        {
            (clust.senses).resize(++clt);
            (clust.senses)[clt-1].center = contvec[i];
            (clust.senses)[clt-1].senseNumber = clt;
            (clust.senses)[clt-1].size++;
            senseID[i] = clt;
        }
        else
        {
            senseID[i] = (clust.senses)[id].senseNumber;
            int sz = (clust.senses)[id].size;
            (clust.senses)[id].center = (clust.senses)[id].center + (contvec[i]/(sz*(1.0)));
            (clust.senses)[id].size++, sz++;
            (clust.senses)[id].center = ((clust.senses)[id].center/((sz*(1.0))/(sz-1)));
        }
    }
}