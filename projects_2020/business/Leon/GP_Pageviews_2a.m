%% load data, target & covariate
d=dataset('File','C:\Users\lufkinlj\Desktop\GA_Data.csv','Delimiter',',');
tmp=zeros(numel(d.date),1);
for i = 1:numel(d.date)
    tmp(i) = str2double(d.date{i}(9:10));
end
d.day=tmp;
clear tmp;
% limit to 2017-2019
d = d((d.year>2016 & d.year<2020),:);
d.day_of_year=(mod((d.t-132),365)+1);
y=d.Pageviews;
n=numel(y);
x=[1:n]';

%figure(1);
%plot(x, y);

%% fixed special days in USA
specdays=[1 1;1 2;2 14;4 1;10 31;12 22;12 23;12 24;12 25;12 26;12 30;12 31];

% construct additional covariates for fixed special days
xs=zeros(n,size(specdays,1));
xsw=zeros(n,size(specdays,1));
for i1=1:size(specdays,1)
  xs(:,i1)=double(d.month==specdays(i1,1)&d.day==specdays(i1,2));
  xsw(:,i1)=double(d.month==specdays(i1,1)&d.day==specdays(i1,2)&d.weekday>=6);
end
% construct additional covariates for floating special days
uyear=unique(d.year);
n=numel(y);
xss=zeros(n,1);
% Labor day
%for i1=1:numel(uyear)
%  q=find(d.year==uyear(i1)&d.month==9&d.weekday==1);
%  xss(q(1),1)=1;
%  xss(q(1)+1,1)=1;
%end
% Thanksgiving
for i1=1:numel(uyear)
  q=find(d.year==uyear(i1)&d.month==11&d.weekday==4);
  xss(q(4),2)=1;
  xss(q(4)+1,2)=1;
end
% Memorial day
%for i1=1:numel(uyear)
%  q=find(d.year==uyear(i1)&d.month==5&d.weekday==1);
%  xss(q(end),3)=1;
%end
% special article days
specartdays1=[760 482 774 58 481 272 59 431 632];
specartdays2=[495 822 628];
xsa1 = zeros(n,1);
xsa2 = xsa1;
xsa1(specartdays1) = 1;
xsa2(specartdays2) = 1;

% combine covariates
x=[[1:n]' xs xsw xss];
m=size(x,2)
x=[x xsa1 xsa2];
% normalize
xn=x;
[yn,ymean,ystd]=normdata(y);

%% priors
pl = prior_logunif();
pn = prior_logunif();

% smooth non-periodic component
%gpcf0 = gpcf_sexp('lengthScale', 365, 'magnSigma2', .1, 'selectedVariables', 1);
% faster changing non-periodic component
gpcf1 = gpcf_sexp('lengthScale', 10, 'magnSigma2', .4, 'selectedVariables', 1);
% periodic component with 7 day period
gpcfp1 = gpcf_periodic('lengthScale', 2, 'magnSigma2', .1, ...
                      'period', 7,'lengthScale_sexp', 20, 'decay', 1, ...
                      'lengthScale_prior', pl, 'magnSigma2_prior', pl, ...
                      'lengthScale_sexp_prior', pl, 'selectedVariables', 1);
% periodic component with 365 day period
gpcfp2 = gpcf_periodic('lengthScale', 6, 'magnSigma2', .7, ... % lengthScale = 5 works well
                      'period', 365,'lengthScale_sexp', 1000, 'decay', 1, ...
                      'lengthScale_prior', pl, 'magnSigma2_prior', pl, ...
                      'lengthScale_sexp_prior', pl, 'selectedVariables', 1);
% linear component for special days
gpcfl1=gpcf_linear('coeffSigma2',1,'selectedVariables',2:m);
% linear component for special article days
gpcfl2=gpcf_linear('coeffSigma2',20,'selectedVariables',m+1);
% linear component for very special article days
gpcfl3=gpcf_linear('coeffSigma2',40,'selectedVariables',m+2);

%% Gaussian model
lik = lik_gaussian('sigma2', 0.1, 'sigma2_prior', pn);
% construct the model
gp = gp_set('lik', lik, 'cf', {gpcf1, gpcfp1, gpcfp2, gpcfl1, gpcfl2, gpcfl3})
% optimise the hyperparameters (MAP)
opt=optimset('TolFun',1e-3,'TolX',1e-4,'Display','iter','DerivativeCheck','off');
gp=gp_optim(gp,xn,yn,'opt',opt);

% Predictions and training log predictive density
[Eft, Varft, lpyt] = gp_pred(gp, xn, yn);sum(lpyt)
% Leave-one-out cross-validation
[Efl, Varfl, lpyl] = gp_loopred(gp, xn, yn);sum(lpyl)

%% Predictions for different components
%[Eft0, Varft0] = gp_pred(gp, xn, yn, 'predcf', 0); % smooth non-periodic component
[Eft1, Varft1] = gp_pred(gp, xn, yn, 'predcf', 1); % faster changing non-periodic component
[Eft2, Varft2] = gp_pred(gp, xn, yn, 'predcf', 2); % periodic component with 7 day period
[Eft3, Varft3] = gp_pred(gp, xn, yn, 'predcf', 3); % periodic component with 365 day period
[Eft4, Varft4] = gp_pred(gp, xn, yn, 'predcf', 4); % linear component for special days
[Eft5, Varft5] = gp_pred(gp, xn, yn, 'predcf', 5); % linear component for special article days
[Eft6, Varft6] = gp_pred(gp, xn, yn, 'predcf', 6); % linear component for very special article days

%% Plot
figure(1);
set(gcf,'units','centimeters');
set(gcf,'pos',[35 2 18.5 24]);
set(gcf,'papertype','a4','paperorientation','portrait',...
'paperunits','centimeters','paperposition',[ 0 0 21.0 29.7]);
clf
% get tight_subplot from
% http://www.mathworks.com/matlabcentral/fileexchange/27991
ha = tight_subplot(4, 1, .04, [.05 .05], [.1 .05])

axes(ha(1))
% Eft1+trend3 = smooth trend from component 1 plus trend from the
%               7 day periodic component
% Eft2 = faster changing non-periodic component
%plot(x(:,1),denormdata(Eft0+trend3,ymean,ystd)/ymean*100,x(:,1),denormdata(Eft2,ymean,ystd)/ymean*100)
plot(x(:,1),denormdata(Eft1,ymean,ystd))%/ymean*100)
set(gca,'xtick',1+cumsum([0 365 365 365]),'xticklabel',2017:1:2020,'xgrid','on','xlim',[-100 1195])
%ylim([77 113])
line(xlim,[ymean ymean],'color', 'r')
%legend('Slow trend','Fast non-periodic component','Mean')
legend('Fast non-periodic component','Mean')
ylabel('Trends')
title('Number of Pageviews on YDN Website')

% compute index for start of each year
ywys=reshape(d.year(1:1092),7,156)';
ywys=ywys(:,[6:7 1:5]);
Y=2017:2019;
for i1=1:numel(Y)
  qi(i1)=find(ywys(:,1)==Y(i1),1);
end

% reshape 7 day periodic component
ywft2s=reshape(Eft2(1:1092),7,156)';
ywft2s=ywft2s(:,[2:6 1 7]);
% trend is not completely seperated to the first smooth component so
% compute the trend in the 7 day periodic component
trend3=interp1(7:7:1094,mean(ywft2s'),1:n)';

% detrend the first periodic component (note that this trend was added to smooth trend above)
ywft2s=denormdata(ywft2s,ymean,ystd);%/ymean*100;
mywft2s=mean(ywft2s,2);
ywft2s=bsxfun(@minus,ywft2s,mywft2s)+ymean;

axes(ha(2))
% ywft2s = 7 day periodic component at different years
plot(ywft2s(qi(1:1:end),:)','-o')
set(gca,'xtick',1:7,'xticklabel',{'Mon' 'Tue' 'Wed' 'Thu' 'Fri' 'Sat' 'Sun'},'xgrid','on')
xlim([-.5 7.5])
%ylim([60 130])
line(xlim,[ymean ymean],'color', 'r')
legend('2017','2018','2019', 'Location', 'southwest')
ylabel('Day of week effect')

% reshape 365 day periodic component
Y=2017:2019;
yyft3s=NaN+zeros(3,365);
for i1=1:numel(Y)
  for i2=1:365
    q=Eft3(d.year==Y(i1)&d.day_of_year==i2);
    if ~isempty(q)
      yyft3s(i1,i2)=q;
    end
  end
end
yyft3s=denormdata(yyft3s,ymean,ystd);%/ymean*100;

axes(ha(3))
% yyft3s = 365 day periodic component at different years
plot(yyft3s(1:1:end,:)','-')
set(gca,'xtick',1+cumsum([0 31 29 31 30 31 30 31 31 30 31 30]),'xticklabel',{'Jan' 'Feb' 'Mar' 'Apr' 'May' 'Jun' 'Jul' 'Aug' 'Sep' 'Oct' 'Nov' 'Dec'},'xgrid','on','xlim', [-86 388])
line(xlim,[ymean ymean],'color', 'r')
%ylim([30 180])
legend('2017','2018','2019', 'Location', 'southwest')
ylabel('Day of year effect')

% reshape special day component
for i1=1:365
  yft4(i1,1)=mean(Eft4(d.day_of_year==i1));
end

%axes(ha(4))
% yft4 = special day effect
%plot(denormdata(yft4,ymean,ystd)/ymean*100,'-')
%set(gca,'xtick',1+cumsum([0 31 29 31 30 31 30 31 31 30 31 30]),'xticklabel',{'Jan' 'Feb' 'Mar' 'Apr' 'May' 'Jun' 'Jul' 'Aug' 'Sep' 'Oct' 'Nov' 'Dec'},'xgrid','on','xlim', [-86 388])
%line(xlim,[100 100],'color', 'r')
%ylabel('Special day effect')
%ylim([99 101])
%yft4d=denormdata(yft4,ymean,ystd)/ymean*100;
%h=text(1,yft4d(1),'New year','HorizontalAlignment','center','VerticalAlignment','top');
%h=text(45,yft4d(45),'Valentine''s day','HorizontalAlignment','center','VerticalAlignment','bottom');
%%h=text(60,yft4d(60),'Leap day','HorizontalAlignment','center','VerticalAlignment','top');
%h=text(92,yft4d(92),'April 1st','HorizontalAlignment','center','VerticalAlignment','top');
%h=text(148,yft4d(148)-10,'Memorial day','HorizontalAlignment','center','VerticalAlignment','top');
%h=text(186,yft4d(186),'Independence day','HorizontalAlignment','center','VerticalAlignment','top');
%h=text(248,yft4d(248)-10,'Labor day','HorizontalAlignment','center','VerticalAlignment','top');
%h=text(305,yft4d(305),'Halloween','HorizontalAlignment','center','VerticalAlignment','top');
%h=text(328,yft4d(328)+5,'Thanksgiving','HorizontalAlignment','center','VerticalAlignment','top');
%h=text(360,yft4d(360),'Christmas','HorizontalAlignment','center','VerticalAlignment','top');

axes(ha(4))
plot(denormdata(Eft6,ymean,ystd),'-')
plot(denormdata(Eft5,ymean,ystd),'-')
set(gca,'xtick',1+cumsum([0 365 365 365]),'xticklabel',2017:1:2020,'xgrid','on','xlim',[-100 1195])
line(xlim,[ymean ymean],'color', 'r')
ylabel('Big article effect')
ylim(10^4*[0.7 4.6])
