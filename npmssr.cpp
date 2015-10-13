#include <iostream>
#include <algorithm>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <map>
#include <vector>
#include <cstring>
#include <string>
#include <ctime>
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

struct sense{
    int senseNumber;
    vector <string> skipGram;
    vector <double> center;
    double size;
};

struct senseList{
    int totalSenses;
    vector <sense> senses;
    double size;
};

map <string, vector <double> > wordvec;
map <string, senseList> multisense;
map <string, int> wordfreq;
map <string, int> stopword;

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

void clean(string &str)
{
    string tmp="";
    int i=0;
    for(i=0;i<str.length();i++)
    {
        if(isalnum(str[i]))
        {
            if((str[i]>='A')&&(str[i]<='Z'))
                str[i]=str[i]-'A'+'a';
            tmp+=str[i];
        }
    }
    str=tmp;
}

void printer(vector <double> arr)
{
    for(int i=0;i<arr.size();i++)
        printf("%.1f ",arr[i]);
    cout<<endl;
}

void printout(senseList arr)
{
    int i=0;
    cout<<"TOTAL CLUSTERS ARE "<<arr.totalSenses<<" "<<arr.size<<endl; 
    for(i=0;i<arr.senses.size();i++)
    {
        cout<<arr.senses[i].senseNumber<<" "<<arr.senses[i].size<<" : ";
        printer(arr.senses[i].center);
    }
}

int recluster(vector <double> contvec, string words, vector <string> skips, double threshold)
{
    int id=0,i,j,senseID;
    double maxa = -10000;
    if(multisense.find(words)==multisense.end())
    {
        senseList clust;
        clust.totalSenses = clust.size = 0;
        multisense.insert(make_pair(words,clust));
    }
    for(j=0;j<(multisense[words].senses).size();j++)
    {   
        double sim = similarity(contvec,(multisense[words].senses)[j].center);
        if(sim>maxa)
        {
            maxa = sim;
            id = j;
        }
    }

    if(maxa < threshold)                                                                                //Define some threshold, discrete model for now
    {
        sense tmp;
        tmp.size = 1;
        tmp.senseNumber = multisense[words].totalSenses;
        tmp.skipGram = skips;
        senseID = multisense[words].totalSenses;
        multisense[words].totalSenses++;
        multisense[words].size++;
        tmp.center = contvec;  
        (multisense[words].senses).push_back(tmp);
    }
    else
    {
        senseID = (multisense[words].senses)[id].senseNumber;
        int sz = (multisense[words].senses)[id].size;
        (multisense[words].senses)[id].center = (multisense[words].senses)[id].center + (contvec/(sz*(1.0)));
        (multisense[words].senses)[id].size++, sz++;
        (multisense[words].senses)[id].center = ((multisense[words].senses)[id].center/((sz*(1.0))/(sz-1)));
        if((multisense[words].senses)[id].skipGram.size()<skips.size())
            (multisense[words].senses)[id].skipGram = skips;
    }

    //if((maxa<0)&&(maxa>-1))
    //    cout<<words<<" "<<maxa<<",,,,";

    if((maxa<threshold)&&(maxa>-1))
    {
        cout<<words<<" : "<<maxa<<", CLUSTERS ARE "<<multisense[words].totalSenses<<",,,,";
        for(j=0;j<(multisense[words].senses).size();j++)
        {    
            for(int k=0;k<(multisense[words].senses)[j].skipGram.size();k++)
                cout<<(multisense[words].senses)[j].skipGram[k]<<" ";
            cout<<endl;
        }
    }

    return senseID;
}

string int2string(int n)
{
    string tmp="",ans="";
    while(n>0)
    {
        tmp+=(n%10)+'0';
        n/=10;
    }
    for(int i=0;i<4-tmp.length();i++)
        ans+='0';
    for(int i=tmp.length()-1;i>=0;i--)
        ans+=tmp[i];
    return ans;
}

int validword(string s)
{
    if(stopword.find(s)!=stopword.end())
        return 0;
    return 1;
}

int main()
{
    srand (time(NULL));

    int maxWindowSize = 5, dim = 50;
    double threshold = -0.45;

    /*

    INPUT WORD VECTORS PART A..... INPUT VOCABULARY..... SELECT TOP 1000-10000 words for clustering

    ASSUME wordvec contains word vectors of all words

    */

    FILE* fi = fopen("huang50rep","r");

    //Format is Number of words, Dimension 
    //string d doubles 
    int numWords;

    int i,j,t,w=0;

    cout<<"SUCCESS\n";

    fscanf(fi,"%d%d",&numWords,&dim);

    cout<<numWords<<" "<<dim<<endl;

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

    fi = fopen("vocab.txt","r");
    
    while(1)
    {
        char str[110];
        fscanf(fi,"%s",str);
        string tmp = string(str);
        int f,waste;
        fscanf(fi,"%d%d",&waste,&f);
        wordfreq.insert(make_pair(tmp,f));
        if(i%10000==0)
            cout<<i<<endl;
        if(feof(fi))
            break;
    }

    fclose(fi);

    cout<<"SUCCESS\n";

    fi = fopen("stopwords","r");
    
    while(1)
    {
        char str[110];
        fscanf(fi,"%s",str);
        string tmp = string(str);
        stopword.insert(make_pair(tmp,1));
        if(feof(fi))
            break;
    }

    fclose(fi);

    cout<<"STOPWORD SUCCESS\n";

    for(int tk = 0; tk < 200; tk++ )
    {
        w=0;
        string ft = "testfiles_sm/tf"+int2string(tk);
        cout<<ft<<endl;
        FILE* fo = fopen(ft.c_str(),"r");
        vector < vector <string> > sent;
        vector < vector <string> > actsent;
        
        //vector < vector <double> > contvec;
        vector <int> senseID;
        vector <string> words;

        string runword="";

        int cnt=0, totalWords=0;
        actsent.resize(++cnt);
        sent.resize(cnt);
        while(1)
        {
            string word;
            ReadWord(word, fo);
            if(feof(fo))
                break;
            if(word == "</s>")
            {
                sent.resize(++cnt);
                sent[cnt-1].push_back(word);
                actsent[cnt-2].push_back(runword);
                runword="";
                actsent.resize(cnt);
                actsent[cnt-1].push_back(word);
                totalWords++;
            }
            else
            {
                clean(word);
                if(validword(word))
                {
                    sent[cnt-1].push_back(word);
                    actsent[cnt-1].push_back(runword+" "+word);
                    runword="";
                    totalWords++;
                }
                else
                    runword+=" "+word;
            }
        }

        fclose(fo);

        cout<<"SUCCESS, total words are : "<<totalWords<<"\n";
        cout<<"Sentences are "<<cnt<<endl;

        //contvec.resize(totalWords+10);
        senseID.resize(totalWords+10);
        
        cout<<"WHAT\n";

        for(i=0;i<sent.size();i++)
        {
            //cout<<"I IS "<<i<<endl;
            for(j=0;j<sent[i].size();j++)
            {
                if(w%300000==0)
                    cout<<"WORDS COMPLETED ARE "<<w<<endl;
                
                senseID[w]=-1;
                words.push_back(sent[i][j]);
                if(wordvec.find(words[w])==wordvec.end())
                {
                    w++;
                    continue;
                }
                else if(wordfreq.find(words[w])==wordfreq.end())
                {
                    w++;
                    continue;
                }
                else if(wordfreq[words[w]]<=22000)
                {
                    w++;
                    continue;
                }                
                //cout<<"GOOD\n";
                vector <double> contvec;
                vector <string> skips;
                int window = rand()%maxWindowSize+2, cnt = 0;
                //cout<<window<<endl;
                InitNULL(contvec,dim);
                for(int k = j-window ; k <= (j+window) ; k++)
                {
                    if(k<0)
                    {
                        contvec=contvec+wordvec["</s>"],skips.push_back("<s>");
                        k=-1;
                    }
                    else if(k>=sent[i].size())
                    {
                        contvec=contvec+wordvec["</s>"],skips.push_back("</s>");
                        cnt++;
                        break;
                    }
                    else if(wordvec.find(sent[i][k])==wordvec.end())
                        contvec=contvec+wordvec["UUUNKKK"];                                                             //UNKNOWN ADDED AFTERWARDS, can also try skipping it
                    else if(k!=j)
                        contvec=contvec+wordvec[sent[i][k]],skips.push_back(actsent[i][k]);
                    else
                        skips.push_back(actsent[i][k]);
                        //cout<<sent[i][k]<<",";
                    cnt++;
                }
                contvec = contvec/(cnt*(1.0));
                //cout<<endl<<sent[i][j]<<endl;
                //printer(contvec[w]);
                if(skips.size()>2)
                    senseID[w] = recluster(/*multisense*/contvec, words[w], skips, threshold);
                w++;
            }
        }

        //printout(clust);
    }

    FILE* fn = fopen("multisenses3","w");

    for( map <string, senseList>::iterator iter = multisense.begin(); iter != multisense.end(); ++iter)
    {
        string k =  iter->first;
        fprintf(fn,"%s %d %d\n",k.c_str(),multisense[k].totalSenses,dim);
        for(i=0;i<((multisense[k].senses).size());i++)
        {
            fprintf(fn,"%d\n",multisense[k].senses[i].senseNumber);
            for(int t=0;t<multisense[k].senses[i].center.size();t++)
                fprintf(fn,"%f ",multisense[k].senses[i].center[t]);
            fprintf(fn,"\n");
        }
    }

    fclose(fn);

    return 0;
}