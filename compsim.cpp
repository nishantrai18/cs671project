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
    return (c/(sqrt(a)*sqrt(b)));
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
        printf("%.1f ",arr[i]);
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

double GlobalSim(string w1, string w2)
{
    vector <double> v1;
    vector <double> v2;
    if(wordvec.find(w1)==wordvec.end())
        v1 = wordvec["UUUNKKK"];
    else
        v1 = wordvec[w1];
    if(wordvec.find(w2)==wordvec.end())
        v2 = wordvec["UUUNKKK"];
    else
        v2 = wordvec[w2];
    return similarity(v1,v2);        
}

double AVGSim(string w1, string w2)
{
    int i,j,t;
    senseList s1, s2;
    if(multisense.find(w1)==multisense.end())
    {
        sense tmp;
        if(wordvec.find(w1)==wordvec.end())
            tmp.center = wordvec["UUUNKKK"];
        else
            tmp.center = wordvec[w1];
        s1.senses.push_back(tmp);
    }
    else
        s1 = multisense[w1],cout<<w1;
    if(multisense.find(w2)==multisense.end())
    {
        sense tmp;
        if(wordvec.find(w2)==wordvec.end())
            tmp.center = wordvec["UUUNKKK"];
        else
            tmp.center = wordvec[w2];
        s2.senses.push_back(tmp);
    }
    else
        s2 = multisense[w2],cout<<w2;
    double scor=0;
    for(i=0;i<s1.senses.size();i++)
    {
        for(j=0;j<s2.senses.size();j++)
            scor+=similarity(s1.senses[i].center,s2.senses[j].center);
    }
    return (scor/(i*j*(1.0)));        
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
    cout<<ma<<" "<<mb<<" "<<sa<<" "<<sb<<" "<<va<<" "<<vb<<endl;
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
    map <string, senseList> multisense;
    cout<<"SUCCESS\n";
    
    FILE* fi;

    //FILE* fn = fopen("multisenses3","r");                                                                       //INPUT MULTISENSE VECTORS
    FILE* fn = fopen("server_data/multisenses6","r");                                                                       //INPUT MULTISENSE VECTORS
    while(!feof(fn))
    {
        char str[110];
        int totsense,dim;
        fscanf(fn,"%s %d %d",str,&totsense,&dim);
        senseList some;
        some.totalSenses = totsense;
        for(i=0;i<totsense;i++)
        {
            int a,b;
            sense tmp;
            fscanf(fn,"%d",&a);
            tmp.senseNumber = a;
            tmp.center.resize(dim);
            for(int t=0;t<dim;t++)
                fscanf(fn,"%lf",&tmp.center[t]);
            some.senses.push_back(tmp);
        }
        multisense.insert(make_pair(string(str),some));
    }
    fclose(fn);
    


    //fi = fopen("npmssr50d.txt","r");
    fi = fopen("huang50rep","r");
    //fi = fopen("googvecs","r");
    
    cout<<"SUCCESS\n";

    fscanf(fi,"%d%d",&numWords,&dim);
    cout<<numWords<<" "<<dim<<endl;
    
    for(i=0 ; i < numWords ; i++)                                                                                   //INPUT GLOBAL VECTORS
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
    vector <double> vec;
    vec.resize(dim);
    InitNULL(vec,dim);
    if(wordvec.find("UUUNKKK")==wordvec.end())
        wordvec.insert(make_pair("UUUNKKK",vec));
    
    /*for(i=0 ; i < numWords ; i++)                                                                                   //INPUT GLOBAL VECTORS
    {
        char str[110];
        int a;
        fscanf(fi,"%s %d",str,&a);
        string tmp = string(str);
        //cout<<str<<","<<a<<":";
        vector <double> vec;
        vec.resize(dim);
        for(j=0;j<dim;j++)
            fscanf(fi,"%lf",&vec[j]);
        wordvec.insert(make_pair(tmp,vec));
        double tf;
        for(j=0;j<2*a;j++)
            for(int tj=0;tj<dim;tj++)
                fscanf(fi,"%lf",&tf);
        if(i%10000==0)
            cout<<i<<endl;
    }*/
    fclose(fi);
    
    cout<<"SUCCESS\n";
    i=0;
    /*fi = fopen("vocab.txt","r");                                                                                    //INPUT VOCAB FREQUENCY
    while(1)
    {
        char str[110];
        fscanf(fi,"%s",str);
        string tmp = string(str);
        int f,waste;
        //fscanf(fi,"%d%d",&waste,&f);
        wordfreq.insert(make_pair(tmp,20000-i));
        if(i%10000==0)
            cout<<i<<endl;
        if(feof(fi))
            break;
        i+=1;
    }
    fclose(fi);
    */

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

    //contvec.resize(totalWords+10);
    //senseID.resize(totalWords+10);

    cout<<"WHAT\n";

    /*for(i=0;i<2;i++)
    {
        //cout<<"I IS "<<i<<endl;
        for(j=5;j<sent[i].size();j++)
        {
            cout<<sent[i][j]<<":"<<seq[i][j]<<" ";
        }
        cout<<endl;
    }*/

    vector <double> s1;
    vector <double> s2;
    vector <double> s3;
    
    for(i=0;i<sent.size()-1;i++)
    {
        //cout<<"I IS "<<i<<endl;
        vector <string> target;
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
            /*vector <double> contvec;
            vector <string> skips;
            int window = rand()%maxWindowSize+2, cnt = 0;
            //cout<<window<<endl;
            InitNULL(contvec,dim);
            for(int k = j-window ; k <= (j+window) ; k++)
            {
                if(k<0)
                {
                    contvec=contvec+wordvec["<s>"],skips.push_back("<s>");
                    k=-1;
                }
                else if(k>=sent[i].size())
                {
                    contvec=contvec+wordvec["</s>"],skips.push_back("</s>");
                    cnt++;
                    break;
                }
                else if(wordvec.find(sent[i][k])==wordvec.end())
                    cnt--;
                else if(k!=j)
                    contvec=contvec+wordvec[sent[i][k]],skips.push_back(sent[i][k]);
                else
                    skips.push_back(sent[i][k]);
                    //cout<<sent[i][k]<<",";
                cnt++;
            }
            contvec = contvec/(cnt*(1.0));
            printer(contvec);
            printer_string(skips);
            */
            target.push_back(sent[i][j]);
            w++;
        }
        cout<<target[0]<<":::"<<target[1]<<"  ";
        cout<<flush;
        double globsim = GlobalSim(target[0],target[1]);
        double avgsim = AVGSim(target[0],target[1]);
        j = sent[i].size()-11;
        //cout<<sent[i][j]<<endl;
        double scor = atof(sent[i][j].c_str());
        cout<<avgsim<<","<<globsim<<":"<<scor<<"\n";
        s1.push_back(avgsim);
        s3.push_back(globsim);
        s2.push_back(scor);
    }

    cout<<"For avgsim we have\n";
    cout<<pearson(s1,s2)<<endl;    
    cout<<spearman(s1,s2)<<endl;
    cout<<"For globsim we have\n";
    cout<<pearson(s3,s2)<<endl;    
    cout<<spearman(s3,s2)<<endl;

    return 0;
}