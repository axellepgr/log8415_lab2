import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.util.*;


public class FriendRecommendation {

    public static class Map extends Mapper<LongWritable, Text, LongWritable, MutualFriendsWritable> {

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            //This section is the processing of one line 
            //In the format: userId friendId1, firendId2, friendsId3 ...
            String line[] = value.toString().split("\t");
            Long fromUser = Long.parseLong(line[0]);
            //list of first degree friends of the user
            List<Long> toUsers = new ArrayList<Long>();

            if (line.length == 2) {
                StringTokenizer tokenizer = new StringTokenizer(line[1], ",");
                //go throw all the 1st degree friends
                while (tokenizer.hasMoreTokens()) {
                    Long toUser = Long.parseLong(tokenizer.nextToken());
                    toUsers.add(toUser);
                    //add the a relationship between the user and his first degree friend
                    //by witing it to the contex by adding a -1 means they are first degree friends
                    //so that this relationship will not be taken into consideration when chosing mutual friends
                    context.write(new LongWritable(fromUser), new MutualFriendsWritable(toUser, -1L));
                }
                //For all the friends
                //Create a new pair (friendId1, friendId2) since they are mutual 
                //friends through the current user that is being processed aka fromUser
                for (int i = 0; i < toUsers.size(); i++) {
                    for (int j = i + 1; j < toUsers.size(); j++) {
                        context.write(new LongWritable(toUsers.get(i)), new MutualFriendsWritable((toUsers.get(j)), fromUser));
                        context.write(new LongWritable(toUsers.get(j)), new MutualFriendsWritable((toUsers.get(i)), fromUser));
                    }
                }
            }
        }
    }

    //In the map phase we should have something like this:
    //u1 u2, u3
    //1st aka we don't really care
    //(key, val) - the key is just a Long and the value is the MutualFriendWritable
    //(u1, (u2, -1L))
    //(u2, (u3, -1L))
    //2nd deg aka possible recommendation
    //(u2, (u3, u1))
    //(u3, (u2, u1))

    public static class Reduce extends Reducer<LongWritable, MutualFriendsWritable, LongWritable, Text> {
        public void reduce(LongWritable key, Iterable<MutualFriendsWritable> values, Context context)
                throws IOException, InterruptedException {

            // for each recommanded friend hol a list of the mutal friends
            //Our goal is to pick the second degree friend with the most mutual friends
            //final is important because the same list is used by all the workers
            final java.util.Map<Long, List<Long>> mutualFriends = new HashMap<Long, List<Long>>();
            //All the writable that share a key
            for (MutualFriendsWritable val : values) {
                final Long toUser = val.user;
                final Long mutualFriend = val.mutualFriend;

                if (mutualFriends.containsKey(toUser)) {
                    if (mutualFriend == -1) {
                        //we nullify the list of common friends if they are already friends
                        mutualFriends.put(toUser, null);
                    } else if (mutualFriends.get(toUser) != null) { //if it is null we don't overide
                        //we append the new recommendation if the they are not friends
                        mutualFriends.get(toUser).add(mutualFriend);
                    }
                } else { //if the hash map does not contain the key to that user we add him
                    //we follow the same logic as above
                    if (mutualFriend != -1) {
                        mutualFriends.put(toUser, new ArrayList<Long>() {
                            {
                                add(mutualFriend);
                            }
                        });
                    } else {
                        mutualFriends.put(toUser, null);
                    }
                }
            }

            //sorting the friends recommandation based on the number of friends
            SortedMap<Long, List<Long>> sortedMutualFriends = new TreeMap<Long, List<Long>>(new Comparator<Long>() {
                public int compare(Long k1, Long k2) {
                    Integer nbrFriends1 = mutualFriends.get(k1).size();
                    Integer nbrFriends2 = mutualFriends.get(k2).size();
                    Integer diff = nbrFriends2 - nbrFriends1;
                    //if it has less number of friends it goes lower in the tree
                    if (diff < 0){
                        return -1;
                    }
                    //if they have the same number of friends return in ascending order
                    if (diff == 0 && k1 < k2){
                        return -1;
                    }
                    return 1;
                }
            });

            for (java.util.Map.Entry<Long, List<Long>> entry : mutualFriends.entrySet()) {
                if (entry.getValue() != null) {
                    sortedMutualFriends.put(entry.getKey(), entry.getValue());
                }
            }

            int i = 0;
            String output = "";
            for (java.util.Map.Entry<Long, List<Long>> entry : sortedMutualFriends.entrySet()) {
                if (i == 0) {
                    output = entry.getKey().toString();
                } else {
                    output += "," + entry.getKey().toString();
                }
                if (i == 9){
                    // we only want the 10 most 
                    break;
                }
                ++i;
            }
            //is the current user that is being parsed
            //will write a tab directly
            //output is the string of mutual friends separated by a comma
            context.write(key, new Text(output));
        }
    }

      static public class MutualFriendsWritable implements Writable {
        public Long user;
        public Long mutualFriend;

        //Creats a new MutualFriendsWritable objects
        //The user id and the list of mutual friends as attributes
        public MutualFriendsWritable(Long user, Long mutualFriend) {
            this.user = user;
            this.mutualFriend = mutualFriend;
        }
        //-1 will mean no relationship
        public MutualFriendsWritable() {
            this(-1L, -1L);
        }

        public void write(DataOutput out) throws IOException {
            out.writeLong(user);
            out.writeLong(mutualFriend);
        }

        public void readFields(DataInput in) throws IOException {
            user = in.readLong();
            mutualFriend = in.readLong();
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();

        Job job = new Job(conf, "FriendRecommendation");
        job.setJarByClass(FriendRecommendation.class);
        job.setOutputKeyClass(LongWritable.class);
        job.setOutputValueClass(MutualFriendsWritable.class);

        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);
        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);
        FileSystem outFs = new Path(args[1]).getFileSystem(conf);
        outFs.delete(new Path(args[1]), true);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        job.waitForCompletion(true);
    }
}
