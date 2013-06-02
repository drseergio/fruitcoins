#import <Foundation/Foundation.h>
#import <PhoneGap/PGPlugin.h>
  

@interface EmptyCookie : PGPlugin {
}

- (void) deleteCookies:(NSMutableArray*)arguments withDict:(NSMutableDictionary*)options;
 

@end