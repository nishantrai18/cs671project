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

vector<double> operator*(const vector<double>& v1, const double& num)
{
    vector <double> tmp;
    for (int i=0;i<v1.size();i++)
    {
        tmp.push_back(v1[i]*num);
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
    vector <double> global;
    double size;
};

map <string, senseList> multisense;
map <string, int> wordfreq;
map <string, int> stopword;
map <string, double> tfidf;

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

void norm(vector <double> &arr)
{
    double a=(0.0000001);
    a=(a*a*a*a*a);
    int i=0;
    for(i=0;i<arr.size();i++)
        a += arr[i]*arr[i];
    a=sqrt(a);
    arr = arr/a;
}

void InitONE(vector <double>& tmp, int size)
{
    tmp.resize(size);
    for(int i=0;i<size;i++)
        tmp[i]=1;
    norm(tmp);
}

double ProbMap(double t)
{
    return (1/(1.000001-t));
}

double similarity(vector <double> arr, vector <double> bar)
{
    double c=0,b=0.00000001,a=0.000000001;
    b=(b*b*b*b*b);
    a=b;
    int i=0;
    for(i=0;i<arr.size();i++)
    {
        c += arr[i]*bar[i];
        a += arr[i]*arr[i];
        b += bar[i]*bar[i];
    }
    //cout<<"A IS "<<a<<" B IS "<<b<<endl;
    double t = (c/(sqrt(a)*sqrt(b)));
    return t;
}

double sigmoid(vector <double> arr, vector <double> bar)
{
    double tmp = similarity(arr, bar);
    return (1.0/(1 + exp(-tmp)));
}

void clean(string &str)
{
    if((str=="<b>")||(str=="</b>"))
        return;
    string tmp="";
    int i=0;
    for(i=0;i<str.length();i++)
    {
        if(isalnum(str[i])||(str[i]=='.')||(str[i]=='-'))
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
        printf("%.2f ",arr[i]);
    cout<<endl;
}

void printer_string(vector <string> arr)
{
    for(int i=0;i<arr.size();i++)
        cout<<arr[i]<<" ";
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
    cout<<"THE GLOBAL VECTOR IS : \n";
    printer(arr.global);
}

string int2string(int n)
{
    string tmp="";
    while(n>0)
    {
        tmp+=(n%10)+'0';
        n/=10;
    }
    reverse(tmp.begin(),tmp.end());
    return tmp;
}

int validword(string s)
{
    if(stopword.find(s)!=stopword.end())
        return 0;
    return 1;
}

double AVGSim(string w1, string w2)
{
    int i,j,t;
    senseList s1, s2;
    
    if(multisense.find(w1)==multisense.end())
        //cout<<"NOT FOUND ";
        s1 = multisense["UUUNKKK"];
    else
        s1 = multisense[w1];
    if(multisense.find(w2)==multisense.end())
        //cout<<"NOT FOUND ";
        s2 = multisense["UUUNKKK"];
    else
        s2 = multisense[w2];
    double scor=0;
    for(i=0;i<s1.senses.size();i++)
    {
        for(j=0;j<s2.senses.size();j++)
            scor+=similarity(s1.senses[i].center,s2.senses[j].center);
    }
    return (scor/(i*j*(1.0)));        
}

double GlobalSim(string w1, string w2)
{
    vector <double> v1;
    vector <double> v2;
    if(multisense.find(w1)==multisense.end())
        v1 = multisense["UUUNKKK"].global;
    else
        v1 = multisense[w1].global;
    if(multisense.find(w2)==multisense.end())
        v2 = multisense["UUUNKKK"].global;
    else
        v2 = multisense[w2].global;
    return similarity(v1,v2);        
}

void ComputeProb(vector <double> c, senseList s, vector <double> &prob)
{
    double sum=0;
    
    //cout<<"THE SIZE OF SENSES IS "<<s.totalSenses<<endl;
    //printer(c);
        
    for(int i=0;i<s.senses.size();i++)
    {
        //printer(s.senses[i].center);
        double t = similarity(c,s.senses[i].center);
        t = ProbMap(t);
        prob.push_back(t);
        sum += t;
        //cout<<t<<",";
    }
    prob = prob/sum;
    //cout<<"THE TOTAL IS "<<sum<<endl;
}

double AVGSimC(string w1, vector <double> c1, string w2, vector <double> c2)
{
    int i,j,t;
    senseList s1, s2;
    
    if(multisense.find(w1) == multisense.end())
        //cout<<"NOT FOUND ";
        s1 = multisense["UUUNKKK"];
    else
        s1 = multisense[w1];
    if(multisense.find(w2) == multisense.end())
        //cout<<"NOT FOUND IT ";
        s2 = multisense["UUUNKKK"];
    else
        s2 = multisense[w2];
    double scor=0;
    vector <double> prob1, prob2;
    //cout<<"SOME1\n";
    //printf("THE Truth value is : %d\n",multisense.find(w1)==multisense.end());
    //printout(s1);
    ComputeProb(c1,s1,prob1);
    //cout<<"SOME2\n";
    //printf("THE Truth value is : %d\n",multisense.find(w2)==multisense.end());
    //printout(s2);
    ComputeProb(c2,s2,prob2);
    for(i=0;i<s1.senses.size();i++)
    {
        for(j=0;j<s2.senses.size();j++)
            scor+=(prob1[i]*prob2[j]*similarity(s1.senses[i].center,s2.senses[j].center));
    }
    return scor;        
}

double LocSim(string w1, vector <double> c1, string w2, vector <double> c2)
{
    int i,j,t;
    senseList s1, s2;
    
    if(multisense.find(w1)==multisense.end())
        //cout<<"NOT FOUND ";
        s1 = multisense["UUUNKKK"];
    else
        s1 = multisense[w1];
    if(multisense.find(w2)==multisense.end())
        //cout<<"NOT FOUND ";
        s2 = multisense["UUUNKKK"];
    else
        s2 = multisense[w2];

    double scor=0;
    vector <double> prob1, prob2;
    //cout<<"SOME1\n";
    ComputeProb(c1,s1,prob1);
    //cout<<"SOME2\n";
    ComputeProb(c2,s2,prob2);
    int mi = 0, mj = 0;
    double mp = 0;
    for(i=0;i<s1.senses.size();i++)
        if (prob1[i] > mp)
        {
            mp = prob1[i];
            mi = i;
        }
    mp = 0;
    for(j=0;j<s2.senses.size();j++)
        if (prob1[j] > mp)
        {
            mp = prob1[j];
            mj = j;
        }
    return similarity(s1.senses[mi].center,s2.senses[mj].center);        
}

double pearson(vector <double> s1, vector <double> s2)
{
    double ma=0,mb=0,sa=0,sb=0,va=0,vb=0,mab=0,cnt=0;
    for(int i=0;i<s1.size();i++)
    {
        ma+=s1[i];
        mb+=s2[i];
        sa+=(s1[i]*s1[i]);
        sb+=(s2[i]*s2[i]);
        mab+=(s1[i]*s2[i]);
        cnt+=1;
    }
    ma/=cnt;
    mb/=cnt;
    mab/=cnt;
    sa/=cnt;
    sb/=cnt;
    va = sqrt(sa-(ma*ma));
    vb = sqrt(sb-(mb*mb));
    //cout<<ma<<" "<<mb<<" "<<sa<<" "<<sb<<" "<<va<<" "<<vb<<endl;
    return ((mab-(ma*mb))/(va*vb));
}

double spearman(vector <double> s1, vector <double> s2)
{
    double s=0,cnt=0;
    vector <int> r1;
    vector <int> r2;
    vector < pair <double, int> > t1;
    vector < pair <double, int> > t2;    
    for(int i=0;i<s1.size();i++)
    {
        t1.push_back(make_pair(s1[i],i));
        t2.push_back(make_pair(s2[i],i));
        r1.push_back(0);
        r2.push_back(0);
    }
    
    sort(t1.begin(),t1.end());
    sort(t2.begin(),t2.end());
    for(int i=0;i<s1.size();i++)
    {
        r1[t1[i].second] = i;
        r2[t2[i].second] = i;
    }
    for(int i=0;i<s1.size();i++)
    {
        s+=(r1[i]-r2[i])*(r1[i]-r2[i]);
        cnt+=1;
    }
    s = ((6*s)/(((cnt*cnt)-1)*cnt));
    return 1-s;
}

string ExtractRoot(string str)
{
    string ans = "";
    int i = 0;
    while ((i<str.length()) && (str[i] != '_'))
    {
        ans += str[i];
        i += 1;
    }
    return ans;
}

//Run for more iterations to see where it converges
//Also try running with the estimated sense vectors
//Modify code to include other embeddings too in the final output
//Modify clean i.e. weaken clean to allow special characters

int main()
{
    srand (time(NULL));

    int maxWindowSize = 5, dim = 50;
    double threshold = -0.4;

    int numWords;
    int i,j,t,w=0;
    cout<<"SUCCESS\n";
    
    FILE* fi;

    //FILE* fn = fopen("multisenses3","r");                                                                       //INPUT MULTISENSE VECTORS
    //FILE* fn = fopen("server_data/multisenses3n300d_goog6000.vec","r");                                                                       //INPUT MULTISENSE VECTORS
    //FILE* fn = fopen("server_data/multisenses3n50d_huang6000.vec","r");
    //FILE* fn = fopen("server_data/multisenses3n50d_huanglargeB.vec","r");                                                                       //INPUT MULTISENSE VECTORS
    //FILE* fn = fopen("server_data/multisenses3n50d_neelB.vec","r");                                                                       //INPUT MULTISENSE VECTORS
    //FILE* fn = fopen("server_data/npmultisenses50d_huanglargeB.vec","r");                                                                       //INPUT MULTISENSE VECTORS
    FILE* fn = fopen("npneel_vectors_skip_trainbig.txt","r");                                                                       //INPUT MULTISENSE VECTORS
    //FILE* fn = fopen("neel_vectors_skip.txt","r");                                                                       //INPUT MULTISENSE VECTORS
     //FILE* fn = fopen("debugvecs.txt","r");                                                                       //INPUT MULTISENSE VECTORS
   
    fscanf(fn,"%d%d",&numWords,&dim);
    cout<<numWords<<" "<<dim<<endl;
    
    for(i=0 ; i < numWords ; i++)                                                                                   //INPUT GLOBAL VECTORS
    {
        char str[110];
        fscanf(fn,"%s",str);
        string tmp = string(str);
        //cout<<tmp<<":";
        string root = ExtractRoot(tmp);
        //cout<<root<<":";
        vector <double> vec;
        vec.resize(dim);
        for(j=0;j<dim;j++)
            fscanf(fn,"%lf",&vec[j]);
        if (multisense.find(root) == multisense.end())
        {
            senseList some;
            some.totalSenses = some.size = 1;
            some.global = vec;
            sense stmp;
            stmp.senseNumber = 0;
            stmp.center = vec;
            some.senses.push_back(stmp);
            multisense.insert(make_pair(root,some));                
        }
        else
        {
            //cout<<root<<":";
            sense stmp;
            stmp.senseNumber = multisense[root].totalSenses;
            stmp.center = vec;
            multisense[root].global = (multisense[root].global)*(multisense[root].totalSenses*(1.0)); 
            multisense[root].global = multisense[root].global + vec;
            multisense[root].totalSenses++;
            multisense[root].global = (multisense[root].global)/(multisense[root].totalSenses*(1.0)); 
            multisense[root].senses.push_back(stmp);            
        }
        if(i%10000==0)
            cout<<i<<",";
        if(i%100000==0)
            cout<<endl;
    }
    fclose(fn);
    cout<<endl;

    /*for(map<string, senseList> iterator = multisense.begin(); iterator != multisense.end(); iterator++) 
    {
        string tmp = iterator->first;
        InitNULL(multisense[tmp].global,dim);
        for(int i=0;i<multisense[tmp].senses.size();i++)
        {
            multisense[tmp].global = multisense[tmp].global +  multisense[tmp].senses[i].center;
        }
        multisense[tmp].global = multisense[tmp].global/(multisense[tmp].senses.size()*(1.0)); 
    }*/

    //printf("THE Truth value is : %d\n",multisense.find("brazil")==multisense.end());
    vector <double> vec;
    vec.resize(dim);
    sense stmp;
    stmp.senseNumber = 0;        
    InitNULL(stmp.center,dim);
    stmp.center[0] = 1;
    senseList some;
    some.totalSenses = some.size = 1;
    some.global = stmp.center;
    some.senses.push_back(stmp);            
    if(multisense.find("UUUNKKK")==multisense.end())
        multisense.insert(make_pair("UUUNKKK",some));
    
    //printout(multisense["UUUNKKK"]);
    //printout(multisense["brazil"]);

    fi = fopen("vocab.txt","r");
    
    FILE* ft = fopen("tfidf.txt","r");
    
    i=0;
    while(1)
    {
        char str[110];
        fscanf(fi,"%s",str);
        string tmp = string(str);
        int f,waste;
        double tfd;
        //fscanf(fi,"%d%d",&waste,&f);
        fscanf(ft,"%lf",&tfd);
        wordfreq.insert(make_pair(tmp,6000-i));
        tfidf.insert(make_pair(tmp,tfd));        
        if(i%10000==0)
            cout<<i<<endl;
        if(feof(fi))
            break;
        i+=1;
    }

    fclose(fi);
    fclose(ft);

    cout<<"SUCCESS\n";
    fi = fopen("stopwords","r");                                                                                    //INPUT STOPWORDS
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
    w=0;
    FILE* fo = fopen("ratings.txt","r");
    vector < vector <string> > sent;
    vector < vector <int> > seq;
    //vector < vector <double> > contvec;
    vector <int> senseID;
    vector <string> words;

    string runword="";

    int cnt=0, totalWords=0, fg=0;
    seq.resize(++cnt);
    sent.resize(cnt);
    while(1)
    {
        string word;
        ReadWord(word, fo);
        if(feof(fo))
            break;
        if(word == "<b>")
        {
            fg=1;
        }
        else if(word == "</b>")
        {
            fg=0;
        }
        else if(word == "</s>")
        {
            sent.resize(++cnt);
            //sent[cnt-1].push_back(word);
            seq.resize(cnt);
            //seq[cnt-1].push_back(0);
            totalWords++;
            //cout<<endl;
        }
        else
        {
            clean(word);
            if(fg)
            {
                sent[cnt-1].push_back(word);
                seq[cnt-1].push_back(1);
                totalWords++;
            }
            else if(validword(word))
            {
                sent[cnt-1].push_back(word);
                seq[cnt-1].push_back(0);
                totalWords++;
                //cout<<word<<",";
            }
        }
    }

    fclose(fo);

    cout<<"SUCCESS, total words are : "<<totalWords<<"\n";
    cout<<"Sentences are "<<cnt<<endl;

    vector <double> s1, s2, s3, s4, s5;
    
    for(i=0;i<sent.size()-1;i++)
    {
        //cout<<"I IS "<<i<<endl;
        vector <string> target;
        vector < vector <double> > contexts;
        for(j=5;j<sent[i].size();j++)
        {
            if(w%300000==0)
                cout<<"WORDS COMPLETED ARE "<<w<<endl;
            words.push_back(sent[i][j]);
            if(seq[i][j]==0)
            {
                w++;
                continue;
            }
            target.push_back(sent[i][j]);
            //cout<<"GOOD\n";
            vector <double> contvec;
            vector <string> skips;
            //int window = rand()%maxWindowSize+2, cnt = 0;
            int window = 5, cnt = 0;
            InitNULL(contvec,dim);
            for(int k = j-window ; k <= (j+window) ; k++)
            {
                //cout<<k<<" : "<<sent[i].size()<<endl;
                if(k<0)
                {
                    if(multisense.find("<s>")!=multisense.end())
                        contvec=contvec+(multisense["<s>"].global)*tfidf["<s>"],skips.push_back("<s>");
                    k=-1;
                }
                else if(k>=sent[i].size())
                {
                    if(multisense.find("</s>")!=multisense.end())
                        contvec=contvec+(multisense["</s>"].global)*tfidf["</s>"],skips.push_back("</s>");
                    break;
                }
                else if(multisense.find(sent[i][k]) == multisense.end())
                    continue;
                    //contvec=contvec+wordvec["UUUNKKK"]*tfidf["UUUNKKK"];                                                             //UNKNOWN ADDED AFTERWARDS, can also try skipping it
                else if(tfidf.find(sent[i][k])==tfidf.end())
                    continue;
                    //contvec=contvec+wordvec["UUUNKKK"]*tfidf["UUUNKKK"];                                                             //UNKNOWN ADDED AFTERWARDS, can also try skipping it
                else if(tfidf[sent[i][k]] < 2)
                    continue;                
                else if(k!=j)
                {   
                    //contvec=contvec+(wordvec[sent[i][k]]*tfidf[sent[i][k]]);
                    if(multisense.find(sent[i][j]) == multisense.end())
                        contvec=contvec+(multisense[sent[i][k]].global*tfidf[sent[i][k]])*(1.0/window);
                    else
                        contvec=contvec+(multisense[sent[i][k]].global*tfidf[sent[i][k]])*similarity(multisense[sent[i][k]].global,multisense[sent[i][j]].global);                        
                }
            }
            norm(contvec);
            //printer(contvec);
            contexts.push_back(contvec);
            w++;
        }
        //cout<<target[0]<<":::"<<target[1]<<"  ";
        //cout<<flush;
        double globsim = GlobalSim(target[0],target[1]);
        double avgsim = AVGSim(target[0],target[1]);
        //cout<<contexts.size()<<" AND YORO\n";
        //printer(contexts[0]);
        //printer(contexts[1]);
        double avgsimc = AVGSimC(target[0],contexts[0],target[1],contexts[1]);
        //cout<<"AVGSIMC "<<avgsimc<<endl;
        double locsim = LocSim(target[0],contexts[0],target[1],contexts[1]);
        //cout<<"LOCSIM "<<locsim<<endl;
        j = sent[i].size()-11;
        //cout<<sent[i][j]<<endl;
        double scor = atof(sent[i][j].c_str());
        //cout<<avgsim<<","<<globsim<<","<<avgsimc<<","<<locsim<<":"<<scor<<"\n";
        s2.push_back(avgsim);
        s3.push_back(globsim);
        s4.push_back(avgsimc);
        s5.push_back(locsim);
        s1.push_back(scor);
    }

    cout<<"For avgsim we have\n";
    cout<<pearson(s2,s1)<<endl;    
    cout<<spearman(s2,s1)<<endl;
    cout<<"For globsim we have\n";
    cout<<pearson(s3,s1)<<endl;    
    cout<<spearman(s3,s1)<<endl;
    cout<<"For avgsimc we have\n";
    cout<<pearson(s4,s1)<<endl;    
    cout<<spearman(s4,s1)<<endl;
    cout<<"For locsim we have\n";
    cout<<pearson(s5,s1)<<endl;    
    cout<<spearman(s5,s1)<<endl;

    return 0;
}