#import "EmptyCookie.h" 
          
@implementation EmptyCookie

-(void) deleteCookies:(NSMutableArray*)arguments withDict:(NSMutableDictionary*)options  
{
  NSHTTPCookie *cookie;
  NSHTTPCookieStorage *storage = [NSHTTPCookieStorage sharedHTTPCookieStorage];
  for (cookie in [storage cookies]) {
    [storage deleteCookie:cookie];
  }
}

@end